import csv
import statistics
from collections import defaultdict

source = "results/combined-results.csv"
output = "results/statistical-summary.csv"

groups = defaultdict(list)

with open(source, newline="") as f:
    for row in csv.DictReader(f):
        key = (
            row["environment"],
            row["benchmark"],
            row["metric"],
            row["unit"],
        )
        groups[key].append(float(row["value"]))

with open(output, "w", newline="") as f:
    fields = [
        "environment", "benchmark", "metric", "unit",
        "runs", "mean", "std_dev", "minimum", "maximum"
    ]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for (environment, benchmark, metric, unit), values in groups.items():
        writer.writerow({
            "environment": environment,
            "benchmark": benchmark,
            "metric": metric,
            "unit": unit,
            "runs": len(values),
            "mean": f"{statistics.mean(values):.6f}",
            "std_dev": f"{statistics.stdev(values):.6f}",
            "minimum": f"{min(values):.6f}",
            "maximum": f"{max(values):.6f}",
        })

print(f"Saved: {output}")
print("\nStatistical summary")
print("-" * 78)

for key, values in groups.items():
    environment, benchmark, metric, unit = key
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    print(
        f"{benchmark:6} | {metric:12} | {environment:22} "
        f"| mean={mean:.4f} {unit} | SD={sd:.4f}"
    )
