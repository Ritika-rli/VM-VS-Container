import hashlib
import time

data = b"VM versus Docker benchmark " * 100
iterations = 500_000

start = time.perf_counter()
result = hashlib.sha256(data).digest()

for i in range(iterations):
    result = hashlib.sha256(result + data).digest()

elapsed = time.perf_counter() - start

print(f"Iterations: {iterations}")
print(f"Elapsed seconds: {elapsed:.4f}")
print(f"Checksum: {result.hex()}")
