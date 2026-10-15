import time

SIZE_MB = 256
data = bytearray(SIZE_MB * 1024 * 1024)

for i in range(0, len(data), 4096):
    data[i] = 1

print(f"Allocated memory: {SIZE_MB} MiB")
print(f"Bytes allocated: {len(data)}")
print(f"Checksum: {sum(data)}")

time.sleep(2)
