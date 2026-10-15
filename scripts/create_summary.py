import csv
import os
import statistics
import matplotlib.pyplot as plt

os.makedirs("results/graphs", exist_ok=True)

# Every row represents one recorded benchmark measurement.
rows = []

def add_runs(environment, benchmark, metric, unit, values):
    for run, value in enumerate(values, start=1):
        rows.append({
            "environment": environment,
            "benchmark": benchmark,
            "metric": metric,
            "run": run,
            "value": value,
            "unit": unit
        })

# CPU: seconds
add_runs("macOS Host", "CPU", "elapsed_time", "seconds",
         [1.1458, 1.1494, 1.1530])
add_runs("Ubuntu VM", "CPU", "elapsed_time", "seconds",
         [1.1568, 1.1514, 1.1429])
add_runs("Docker in Ubuntu VM", "CPU", "elapsed_time", "seconds",
         [1.1751, 1.2033, 1.1877])

# Memory: wall-clock seconds
add_runs("macOS Host", "Memory", "wall_time", "seconds",
         [3.20, 3.16, 3.15])
add_runs("Ubuntu VM", "Memory", "wall_time", "seconds",
         [3.28, 3.20, 3.20])
add_runs("Docker in Ubuntu VM", "Memory", "wall_time", "seconds",
         [3.20, 3.19, 3.19])

# Disk: seconds; VM and Docker use the preferred bind-path runs.
add_runs("macOS Host", "Disk", "write_time", "seconds",
         [0.4392, 0.0610, 0.0598])
add_runs("Ubuntu VM", "Disk", "write_time", "seconds",
         [0.3040, 0.0942, 0.1209])
add_runs("Docker in Ubuntu VM", "Disk", "write_time", "seconds",
         [0.1354, 0.0757, 0.1084])

add_runs("macOS Host", "Disk", "read_time", "seconds",
         [0.2081, 0.2266, 0.2167])
add_runs("Ubuntu VM", "Disk", "read_time", "seconds",
         [0.1891, 0.1875, 0.1867])
add_runs("Docker in Ubuntu VM", "Disk", "read_time", "seconds",
         [0.1891, 0.1873, 0.1859])

with open("results/combined-results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "environment", "benchmark", "metric", "run", "value", "unit"
    ])
    writer.writeheader()
    writer.writerows(rows)

# Print average measurements.
print("\nAVERAGE RESULTS (seconds)")
groups = {}
for row in rows:
    key = (row["benchmark"], row["metric"], row["environment"])
    groups.setdefault(key, []).append(row["value"])

for (benchmark, metric, environment), values in groups.items():
    print(f"{benchmark:8} {metric:12} {environment:22} "
          f"{statistics.mean(values):.4f}")

# Plot average time per environment.
for benchmark, metrics in {
    "cpu": ["elapsed_time"],
    "memory": ["wall_time"],
    "disk": ["write_time", "read_time"]
}.items():
    for metric in metrics:
        labels = []
        averages = []
        for (b, m, environment), values in groups.items():
            if b.lower() == benchmark and m == metric:
                labels.append(environment)
                averages.append(statistics.mean(values))

        plt.figure(figsize=(9, 5))
        plt.bar(labels, averages)
        plt.ylabel("Average time (seconds)")
        plt.title(f"{benchmark.upper()} Benchmark: {metric.replace('_', ' ').title()}")
        plt.xticks(rotation=15, ha="right")
        plt.tight_layout()
        path = f"results/graphs/{benchmark}-{metric}.png"
        plt.savefig(path, dpi=200)
        plt.close()
        print(f"Graph saved: {path}")

print("\nCSV saved: results/combined-results.csv")
