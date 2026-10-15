# VM vs Container Performance Benchmark

## Overview
This project compares selected benchmark workloads across three environments:
1. Native execution on an Apple M4 MacBook Air running macOS.
2. Ubuntu 24.04.5 LTS running in UTM as a virtual machine.
3. Docker containers running inside the Ubuntu virtual machine.

## Benchmarks
- CPU: SHA-256 computation workload with 500,000 iterations.
- Memory: allocation and touching of 256 MiB, with a fixed two-second sleep.
- Disk: writing and reading 256 MiB of data, with checksum verification.

Each benchmark was repeated ten times. The results include timing measurements, statistical summaries, and graphs.

## Important Limitations
- Docker runs inside the Ubuntu virtual machine, not directly on macOS.
- The native macOS and Linux environments use different Python versions.
- The memory workload's wall-clock time includes a fixed sleep.
- The disk benchmarks use different storage paths across environments.
- Results represent one machine and a limited set of workloads.

## Repository Contents
- `scripts/`: benchmark and analysis scripts.
- `results/`: experiment logs, CSV summaries, and graphs.
- `backup/`: supporting files, if applicable.

## Purpose
This repository supports an academic experimental study of native execution, virtual machines, and containers on Apple Silicon.
