import csv
import re
import statistics
from pathlib import Path

base = Path.home() / "vm-container-host-test"
root = base / "results" / "experiment-10-runs"

# Measurements copied from the completed macOS 10-run experiment.
mac = {
    ("cpu", "elapsed_time"): [
        1.1268, 1.1474, 1.1170, 1.1288, 1.1266,
        1.1429, 1.1307, 1.1256, 1.1330, 1.1178
    ],
    ("memory", "wall_time"): [
        3.22, 3.15, 3.15, 3.14, 3.14,
        3.13, 3.13, 3.14, 3.13, 3.14
    ],
    ("disk", "write_time"): [
        0.0564, 0.0620, 0.0631, 0.0839, 0.0619,
        0.0623, 0.0821, 0.0622, 0.0620, 0.0618
    ],
    ("disk", "read_time"): [
        0.2030, 0.2076, 0.2061, 0.2125, 0.2144,
        0.2084, 0.2113, 0.2073, 0.2064, 0.2068
    ],
}

rows = []

def add_rows(environment, benchmark, metric, values, unit="seconds"):
    for run, value in enumerate(values, start=1):
        rows.append({
            "environment": environment,
            "benchmark": benchmark,
            "metric": metric,
            "run": run,
            "value": value,
            "unit": unit,
        })

for (benchmark, metric), values in mac.items():
    add_rows("macOS host", benchmark, metric, values)

for environment in ("ubuntu-vm", "docker"):
    for benchmark in ("cpu", "memory", "disk"):
        log = root / environment / f"{benchmark}-{environment}-10runs.txt"
        content = log.read_text()

        if benchmark == "cpu":
            metric_values = {
                "elapsed_time": re.findall(
                    r"Elapsed seconds:\s*([\d.]+)", content
                )
            }
        elif benchmark == "memory":
            metric_values = {
                "wall_time": re.findall(
                    r"Outer wall time:\s*([\d.]+)", content
                )
            }
        else:
            metric_values = {
                "write_time": re.findall(
                    r"Write time:\s*([\d.]+)", content
                ),
                "read_time": re.findall(
                    r"Read time:\s*([\d.]+)", content
                ),
            }

        for metric, values in metric_values.items():
            if len(values) != 10:
                raise ValueError(
                    f"{log}: expected 10 values for {metric}, "
                    f"found {len(values)}"
                )
            add_rows(
                environment, benchmark, metric,
                [float(value) for value in values]
            )

combined = root / "combined-results-10runs.csv"
with combined.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "environment", "benchmark", "metric", "run", "value", "unit"
    ])
    writer.writeheader()
    writer.writerows(rows)

summary = root / "statistical-summary-10runs.csv"
groups = {}
for row in rows:
    key = (
        row["environment"], row["benchmark"],
        row["metric"], row["unit"]
    )
    groups.setdefault(key, []).append(float(row["value"]))

summary_rows = []
for (env, benchmark, metric, unit), values in groups.items():
    summary_rows.append({
        "environment": env,
        "benchmark": benchmark,
        "metric": metric,
        "unit": unit,
        "runs": len(values),
        "mean": round(statistics.mean(values), 6),
        "std_dev": round(statistics.stdev(values), 6),
        "minimum": round(min(values), 6),
        "maximum": round(max(values), 6),
    })

with summary.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=summary_rows[0].keys())
    writer.writeheader()
    writer.writerows(summary_rows)

print("Combined raw measurements:", combined)
print("Statistical summary:", summary)
print("\nEnvironment | Benchmark | Metric | Mean (s) | SD (s)")
print("-" * 66)
for row in summary_rows:
    print(
        f"{row['environment']:12} | {row['benchmark']:8} | "
        f"{row['metric']:12} | {row['mean']:.4f} | "
        f"{row['std_dev']:.4f}"
    )

print(f"\nTotal measurements: {len(rows)}")
