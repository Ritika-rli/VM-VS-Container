# VM vs Container Performance Benchmark

## Overview

This project compares three execution environments on an Apple M4 MacBook Air:

1. Native execution on macOS.
2. Ubuntu 24.04.5 LTS running in a UTM virtual machine.
3. Docker containers running inside the Ubuntu virtual machine.

The study measures CPU execution time, memory-workload wall-clock time, and disk read/write time. Each benchmark was repeated ten times.

## System Configuration

- Host: Apple M4 MacBook Air, 16 GB RAM
- Guest OS: Ubuntu 24.04.5 LTS, ARM64
- Virtualization: UTM
- Docker: 29.1.3
- Native Python: 3.14.3
- Ubuntu Python: 3.12.3
- Container base image: python:3.12-slim

## Benchmarks

- CPU: 500,000 iterations of a SHA-256 computation workload.
- Memory: allocate and touch 256 MiB, followed by a fixed two-second sleep.
- Disk: write 256 MiB, synchronize it, read it back, and calculate a SHA-256 checksum.

## Results

The `results/` directory contains experiment logs, CSV files, statistical summaries, and graphs for the recorded runs.

## Limitations

- Docker runs inside the Ubuntu virtual machine, not directly on macOS.
- The native and Linux environments use different Python versions.
- The memory workload's wall time includes a fixed sleep and is not a direct memory-bandwidth measurement.
- Disk tests use different storage paths across environments, so their results are not a fully controlled comparison.
- The experiment uses one physical machine and a limited set of workloads.
- The findings should not be generalized to all virtual machines or containers.

## Repository Structure

- `scripts/`: benchmark, analysis, and plotting scripts.
- `results/`: raw logs, CSV summaries, and graphs.
- `backup/`: additional files not yet included in the tracked project.

## Purpose

This repository supports an academic experimental study comparing native execution, virtual machines, and containers on Apple Silicon.
