import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.meter import WL4000

meter = WL4000(word_order="low_high")

if not meter.connect():
    print("Connection failed.")
    raise SystemExit

times = []

for i in range(10):
    t0 = time.time()
    meter.read_all()
    t1 = time.time()
    elapsed = t1 - t0
    times.append(elapsed)
    print(f"Read {i+1}: {elapsed:.3f}s")

meter.disconnect()

avg = sum(times) / len(times)
print(f"\nAverage: {avg:.3f}s per full read ({1/avg:.2f} reads/sec)")