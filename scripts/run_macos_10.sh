#!/bin/bash
set -e

BASE="$HOME/vm-container-host-test"
OUT="$BASE/results/experiment-10-runs/macos"

cd "$BASE"
mkdir -p "$OUT"

for benchmark in cpu memory disk; do
    SCRIPT="$BASE/scripts/${benchmark}_benchmark.py"
    LOG="$OUT/${benchmark}-macos-10runs.txt"

    if [ ! -f "$SCRIPT" ]; then
        echo "Missing benchmark script: $SCRIPT"
        exit 1
    fi

    echo "Running $benchmark benchmark 10 times..."
    : > "$LOG"

    for i in $(seq 1 10); do
        echo "===== macOS $benchmark run $i =====" | tee -a "$LOG"
        python3 "$SCRIPT" 2>&1 | tee -a "$LOG"
    done

    echo "Saved: $LOG"
done

echo "All macOS benchmarks completed."
