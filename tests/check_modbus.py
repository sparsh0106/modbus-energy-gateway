import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.client import ModbusGateway

gateway = ModbusGateway()
gateway.connect()

result = gateway.client.read_holding_registers(address=158, count=4, device_id=1)
print(result.registers)

gateway.disconnect()