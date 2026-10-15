import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = Path.home() / "vm-container-host-test"
root = base / "results" / "experiment-10-runs"
summary_file = root / "statistical-summary-10runs.csv"
graph_dir = root / "graphs"
graph_dir.mkdir(parents=True, exist_ok=True)

with summary_file.open(newline="") as f:
    rows = list(csv.DictReader(f))

environments = ["macOS host", "ubuntu-vm", "docker"]
labels = ["macOS Host", "Ubuntu VM", "Docker in Ubuntu VM"]

charts = [
    ("cpu", "elapsed_time", "CPU Benchmark", "Elapsed time (seconds)", "cpu"),
    ("memory", "wall_time", "Memory Benchmark", "Wall time (seconds)", "memory"),
    ("disk", "write_time", "Disk Write Benchmark", "Write time (seconds)", "disk-write"),
    ("disk", "read_time", "Disk Read Benchmark", "Read time (seconds)", "disk-read"),
]

for benchmark, metric, title, ylabel, filename in charts:
    selected = {
        row["environment"]: row
        for row in rows
        if row["benchmark"] == benchmark and row["metric"] == metric
    }

    means = [float(selected[e]["mean"]) for e in environments]
    errors = [float(selected[e]["std_dev"]) for e in environments]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(
        labels,
        means,
        yerr=errors,
        capsize=6,
    )

    ax.set_title(f"{title}: 10 Runs per Environment")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Execution environment")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    for bar, mean in zip(bars, means):
        ax.annotate(
            f"{mean:.4f}s",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    fig.tight_layout()
    path = graph_dir / f"{filename}-10runs.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")

print("\nAll four graphs generated.")
