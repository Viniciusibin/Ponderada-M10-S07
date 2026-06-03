"""
Metrics collector — calls GitHub Actions API to build metrics.csv.

Usage:
    export GITHUB_TOKEN=ghp_...
    python scripts/collect_metrics.py --repo OWNER/REPO

Output:
    data/metrics.csv
    data/metrics_jobs.csv
"""
import argparse
import csv
import json
import os
import sys
import zipfile
import io
from datetime import datetime, timezone

import requests

BASE_URL = "https://api.github.com"


def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: Set GITHUB_TOKEN env var before running.", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def paginate(url, headers, params=None):
    results = []
    page = 1
    while True:
        p = dict(params or {})
        p["per_page"] = 100
        p["page"] = page
        resp = requests.get(url, headers=headers, params=p)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            items = data.get("workflow_runs") or data.get("jobs") or []
        else:
            items = data
        if not items:
            break
        results.extend(items)
        if len(items) < 100:
            break
        page += 1
    return results


def duration_seconds(start, end):
    if not start or not end:
        return None
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    try:
        s = datetime.strptime(start, fmt).replace(tzinfo=timezone.utc)
        e = datetime.strptime(end, fmt).replace(tzinfo=timezone.utc)
        return round((e - s).total_seconds(), 1)
    except Exception:
        return None


def fetch_run_artifact_metadata(repo, run_id, headers):
    url = f"{BASE_URL}/repos/{repo}/actions/runs/{run_id}/artifacts"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {}
    artifacts = resp.json().get("artifacts", [])
    for art in artifacts:
        if art["name"].startswith("run-metrics-"):
            dl_url = art["archive_download_url"]
            dl = requests.get(dl_url, headers=headers, allow_redirects=True)
            if dl.status_code == 200:
                try:
                    with zipfile.ZipFile(io.BytesIO(dl.content)) as z:
                        for name in z.namelist():
                            if name.endswith(".json"):
                                with z.open(name) as f:
                                    return json.load(f)
                except Exception:
                    pass
    return {}


def collect(repo):
    headers = get_headers()

    print(f"Fetching workflow runs for {repo}...")
    runs_url = f"{BASE_URL}/repos/{repo}/actions/runs"
    runs = paginate(runs_url, headers, {"branch": "main"})
    print(f"Found {len(runs)} runs.")

    workflow_rows = []
    job_rows = []

    for run in runs:
        run_id = run["id"]
        commit_sha = run["head_sha"]
        commit_message = (run.get("head_commit") or {}).get("message", "").split("\n")[0]
        status = run["conclusion"] or run["status"]
        created_at = run["created_at"]
        updated_at = run["updated_at"]
        workflow_duration = duration_seconds(created_at, updated_at)

        artifact_meta = fetch_run_artifact_metadata(repo, run_id, headers)
        test_count = artifact_meta.get("test_count", "")
        test_failures = artifact_meta.get("test_failures", "")
        test_duration = artifact_meta.get("test_duration_seconds", "")

        jobs_url = f"{BASE_URL}/repos/{repo}/actions/runs/{run_id}/jobs"
        jobs_resp = requests.get(jobs_url, headers=headers)
        jobs = jobs_resp.json().get("jobs", []) if jobs_resp.status_code == 200 else []

        for job in jobs:
            job_name = job["name"]
            job_duration = duration_seconds(job.get("started_at"), job.get("completed_at"))
            job_status = job.get("conclusion") or job.get("status")

            job_rows.append({
                "run_id": run_id,
                "commit_sha": commit_sha[:8],
                "job_name": job_name,
                "job_status": job_status,
                "job_duration": job_duration,
                "timestamp": created_at,
            })

            workflow_rows.append({
                "run_id": run_id,
                "commit_sha": commit_sha[:8],
                "commit_message": commit_message,
                "status": status,
                "workflow_duration": workflow_duration,
                "job_name": job_name,
                "job_duration": job_duration,
                "test_count": test_count,
                "test_failures": test_failures,
                "test_duration": test_duration,
                "timestamp": created_at,
            })

    os.makedirs("data", exist_ok=True)

    main_fields = [
        "run_id", "commit_sha", "commit_message", "status",
        "workflow_duration", "job_name", "job_duration",
        "test_count", "test_failures", "test_duration", "timestamp",
    ]
    with open("data/metrics.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=main_fields)
        w.writeheader()
        workflow_rows.sort(key=lambda r: r["timestamp"])
        w.writerows(workflow_rows)
    print(f"Saved data/metrics.csv ({len(workflow_rows)} rows)")

    job_fields = [
        "run_id", "commit_sha", "job_name", "job_status", "job_duration", "timestamp",
    ]
    with open("data/metrics_jobs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=job_fields)
        w.writeheader()
        job_rows.sort(key=lambda r: r["timestamp"])
        w.writerows(job_rows)
    print(f"Saved data/metrics_jobs.csv ({len(job_rows)} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect GitHub Actions metrics")
    parser.add_argument("--repo", required=True, help="owner/repo")
    args = parser.parse_args()
    collect(args.repo)
