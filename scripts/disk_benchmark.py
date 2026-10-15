import os
import time
import hashlib

FILE_PATH = "/tmp/vm_container_disk_test.bin"
SIZE_MB = 256
CHUNK_SIZE = 1024 * 1024
CHUNK = b"A" * CHUNK_SIZE

# Write benchmark
start = time.perf_counter()

with open(FILE_PATH, "wb") as f:
    for _ in range(SIZE_MB):
        f.write(CHUNK)
    f.flush()
    os.fsync(f.fileno())

write_seconds = time.perf_counter() - start

# Read benchmark
start = time.perf_counter()
digest = hashlib.sha256()

with open(FILE_PATH, "rb") as f:
    while True:
        block = f.read(CHUNK_SIZE)
        if not block:
            break
        digest.update(block)

read_seconds = time.perf_counter() - start

print(f"File size: {SIZE_MB} MiB")
print(f"Write time: {write_seconds:.4f} seconds")
print(f"Read time: {read_seconds:.4f} seconds")
print(f"SHA-256: {digest.hexdigest()}")

os.remove(FILE_PATH)
