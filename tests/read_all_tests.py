import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.meter import WL4000

meter = WL4000()

if not meter.connect():
    print("Connection failed.")
    raise SystemExit

values = meter.read_all()

meter.disconnect()

for name, data in values.items():
    if data["error"]:
        print(f"{name:20} ERROR: {data['error']}")
    else:
        print(f"{name:20} {data['value']:.3f} {data['unit']}")