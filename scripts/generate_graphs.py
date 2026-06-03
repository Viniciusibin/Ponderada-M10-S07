"""
Generate 4 required graphs from data/metrics.csv.

Usage:
    python scripts/generate_graphs.py

Output: graphs/graph_01_*.png ... graph_04_*.png
"""
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

METRICS_CSV = "data/metrics.csv"
JOBS_CSV = "data/metrics_jobs.csv"
OUT_DIR = "graphs"


def load_data():
    if not os.path.exists(METRICS_CSV):
        print(f"ERROR: {METRICS_CSV} not found. Run collect_metrics.py first.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(METRICS_CSV)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["run_number"] = df.groupby("run_id").ngroup() + 1
    return df


def load_jobs():
    if not os.path.exists(JOBS_CSV):
        return None
    df = pd.read_csv(JOBS_CSV)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def graph_01_pipeline_duration(df):
    """Total pipeline duration per run (line chart)."""
    runs = (
        df.groupby(["run_id", "commit_sha", "commit_message", "status", "timestamp"])
        ["workflow_duration"]
        .first()
        .reset_index()
        .sort_values("timestamp")
    )
    runs["run_number"] = range(1, len(runs) + 1)

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = ["#2ecc71" if s == "success" else "#e74c3c" for s in runs["status"]]
    ax.bar(runs["run_number"], runs["workflow_duration"], color=colors, edgecolor="white")
    ax.plot(runs["run_number"], runs["workflow_duration"], "o-", color="#2c3e50", linewidth=1.5)

    ax.set_xlabel("Execução (#)", fontsize=11)
    ax.set_ylabel("Duração total (s)", fontsize=11)
    ax.set_title("Tempo total do pipeline por execução", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    from matplotlib.patches import Patch
    legend = [Patch(facecolor="#2ecc71", label="Sucesso"), Patch(facecolor="#e74c3c", label="Falha")]
    ax.legend(handles=legend)

    short_msgs = [m[:30] + "…" if len(m) > 30 else m for m in runs["commit_message"]]
    ax.set_xticks(runs["run_number"])
    ax.set_xticklabels(short_msgs, rotation=45, ha="right", fontsize=7)

    plt.tight_layout()
    path = f"{OUT_DIR}/graph_01_pipeline_duration.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path}")


def graph_02_job_duration(df_jobs):
    """Duration per job across runs (grouped bar chart)."""
    if df_jobs is None:
        print("Skipping graph_02: metrics_jobs.csv not found")
        return

    df_jobs = df_jobs.sort_values("timestamp")
    df_jobs["run_number"] = df_jobs.groupby("run_id").ngroup() + 1

    pivot = df_jobs.pivot_table(
        index="run_number", columns="job_name", values="job_duration", aggfunc="mean"
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    pivot.plot(kind="bar", ax=ax, edgecolor="white")

    ax.set_xlabel("Execução (#)", fontsize=11)
    ax.set_ylabel("Duração (s)", fontsize=11)
    ax.set_title("Duração por job em cada execução", fontsize=13, fontweight="bold")
    ax.legend(title="Job", bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.tight_layout()
    path = f"{OUT_DIR}/graph_02_job_duration.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path}")


def graph_03_success_rate(df):
    """Success vs failure rate (pie + bar)."""
    runs = df.drop_duplicates("run_id")
    counts = runs["status"].value_counts()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    palette = {"success": "#2ecc71", "failure": "#e74c3c", "cancelled": "#f39c12"}
    colors = [palette.get(s, "#95a5a6") for s in counts.index]

    ax1.pie(counts.values, labels=counts.index, colors=colors, autopct="%1.0f%%",
            startangle=90, textprops={"fontsize": 11})
    ax1.set_title("Taxa de sucesso / falha", fontsize=12, fontweight="bold")

    ax2.bar(counts.index, counts.values, color=colors, edgecolor="white")
    ax2.set_ylabel("Número de execuções", fontsize=11)
    ax2.set_title("Contagem por status", fontsize=12, fontweight="bold")
    for i, (label, val) in enumerate(counts.items()):
        ax2.text(i, val + 0.1, str(val), ha="center", fontweight="bold")

    plt.tight_layout()
    path = f"{OUT_DIR}/graph_03_success_rate.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path}")


def graph_04_tests_vs_duration(df):
    """Scatter: test count × workflow duration, coloured by status."""
    data = df.drop_duplicates("run_id").copy()
    data = data.dropna(subset=["test_count", "workflow_duration"])
    data["test_count"] = pd.to_numeric(data["test_count"], errors="coerce")
    data = data.dropna(subset=["test_count"])

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = {"success": "#2ecc71", "failure": "#e74c3c"}

    for status, group in data.groupby("status"):
        color = palette.get(status, "#95a5a6")
        ax.scatter(group["test_count"], group["workflow_duration"],
                   label=status, color=color, s=80, edgecolors="white", linewidths=0.5)

    ax.set_xlabel("Quantidade de testes", fontsize=11)
    ax.set_ylabel("Duração total do pipeline (s)", fontsize=11)
    ax.set_title("Relação entre quantidade de testes e duração do pipeline", fontsize=12, fontweight="bold")
    ax.legend(title="Status")

    plt.tight_layout()
    path = f"{OUT_DIR}/graph_04_tests_vs_duration.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()
    df_jobs = load_jobs()

    graph_01_pipeline_duration(df)
    graph_02_job_duration(df_jobs)
    graph_03_success_rate(df)
    graph_04_tests_vs_duration(df)
    print("All graphs generated successfully.")


if __name__ == "__main__":
    main()
