import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.client import ModbusGateway

gateway = ModbusGateway()

if not gateway.connect():
    print("Connection failed.")
    raise SystemExit

found = []

for slave_id in range(1, 248):
    print(f"Checking id {slave_id}")
    try:
        response = gateway.client.read_holding_registers(
            address=138,
            count=2,
            device_id=slave_id
        )
        if not response.isError():
            print(f"Found meter {slave_id}")
            found.append(slave_id)
    except Exception:
        pass

gateway.disconnect()

print(f"\nTotal meters found: {len(found)}")
print(found)