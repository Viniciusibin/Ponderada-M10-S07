"""
Inline metadata collector — runs inside GitHub Actions.
Reads env vars injected by the workflow and parses junit XML,
then writes data/run_metadata.json for artifact upload.
"""
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

Path("data").mkdir(exist_ok=True)

run_id = os.environ.get("RUN_ID", "unknown")
commit_sha = os.environ.get("COMMIT_SHA", "unknown")
commit_message = os.environ.get("COMMIT_MESSAGE", "").strip()
workflow_status = os.environ.get("WORKFLOW_STATUS", "unknown")
lint_status = os.environ.get("LINT_STATUS", "unknown")
timestamp = os.environ.get("RUN_TIMESTAMP", "unknown")

test_count = 0
test_failures = 0
test_errors = 0
test_duration = 0.0

junit_path = Path("results/junit.xml")
if junit_path.exists():
    tree = ET.parse(junit_path)
    root = tree.getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is not None:
        test_count = int(suite.get("tests", 0))
        test_failures = int(suite.get("failures", 0))
        test_errors = int(suite.get("errors", 0))
        test_duration = float(suite.get("time", 0.0))

metadata = {
    "run_id": run_id,
    "commit_sha": commit_sha[:8] if len(commit_sha) > 8 else commit_sha,
    "commit_sha_full": commit_sha,
    "commit_message": commit_message,
    "workflow_status": workflow_status,
    "lint_status": lint_status,
    "timestamp": timestamp,
    "test_count": test_count,
    "test_failures": test_failures,
    "test_errors": test_errors,
    "test_duration_seconds": test_duration,
}

output = Path("data/run_metadata.json")
output.write_text(json.dumps(metadata, indent=2))
print(f"Metadata saved: {output}")
print(json.dumps(metadata, indent=2))
