import sys
import struct
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.client import ModbusGateway

gateway = ModbusGateway()

if not gateway.connect():
    print("Connection failed.")
    raise SystemExit

try:
    result = gateway.read(address=138, count=2)  # VLN_AVG only

    if result.isError():
        print("Modbus error:", result)
        raise SystemExit

    regs = result.registers
    print(f"Raw registers: {regs}\n")

    r0, r1 = regs

    combos = {
        "high_low (AB CD)": struct.pack(">HH", r0, r1),
        "low_high (CD AB)": struct.pack(">HH", r1, r0),
        "high_low byte-swapped (BA DC)": struct.pack("<HH", r0, r1)[::-1],
        "low_high byte-swapped (DC BA)": struct.pack("<HH", r1, r0)[::-1],
    }

    for name, packed in combos.items():
        value = struct.unpack(">f", packed)[0]
        print(f"{name:35} {value}")

finally:
    gateway.disconnect()