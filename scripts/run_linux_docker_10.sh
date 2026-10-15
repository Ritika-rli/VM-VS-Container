#!/bin/bash
set -euo pipefail

BASE="$HOME/vm-container-host-test"
OUT="$BASE/results/experiment-10-runs"

cd "$BASE"

# Confirm that the Docker image exists
docker image inspect vm-benchmark:latest >/dev/null

for ENVIRONMENT in ubuntu-vm docker; do
    for BENCHMARK in cpu memory disk; do

        LOG="$OUT/$ENVIRONMENT/${BENCHMARK}-${ENVIRONMENT}-10runs.txt"
        SCRIPT="/work/scripts/${BENCHMARK}_benchmark.py"

        echo "========================================"
        echo "Environment: $ENVIRONMENT"
        echo "Benchmark: $BENCHMARK"
        echo "========================================"

        : > "$LOG"

        for i in $(seq 1 10); do
            echo "===== $ENVIRONMENT $BENCHMARK run $i =====" \
                | tee -a "$LOG"

            if [ "$ENVIRONMENT" = "ubuntu-vm" ]; then
                if [ "$BENCHMARK" = "disk" ]; then
                    export BENCHMARK_FILE="$OUT/ubuntu-vm/disk-run-$i.bin"
                fi

                /usr/bin/time -f "Outer wall time: %e seconds" \
                    python3 "$BASE/scripts/${BENCHMARK}_benchmark.py" \
                    2>&1 | tee -a "$LOG"

                unset BENCHMARK_FILE || true

            else
                docker_args=(
                    run --rm
                    -v "$BASE:/work"
                    -w /work
                )

                if [ "$BENCHMARK" = "disk" ]; then
                    docker_args+=(
                        -e "BENCHMARK_FILE=/work/results/experiment-10-runs/docker/disk-run-$i.bin"
                    )
                fi

                /usr/bin/time -f "Outer wall time: %e seconds" \
                    docker "${docker_args[@]}" \
                    vm-benchmark:latest \
                    python "$SCRIPT" \
                    2>&1 | tee -a "$LOG"
            fi
        done

        echo "Saved: $LOG"
    done
done

echo "All Ubuntu VM and Docker benchmarks completed."
