import json
from pathlib import Path

from pymodbus.client import ModbusSerialClient

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "wl4000.json"


class ModbusGateway:

    def __init__(self, config_path: Path = CONFIG_PATH):
        with open(config_path) as f:
            cfg = json.load(f)

        self.device_id = cfg.get("device_id", 12)

        self.client = ModbusSerialClient(
            port=cfg["port"],
            baudrate=cfg["baudrate"],
            parity=cfg["parity"],
            stopbits=cfg["stopbits"],
            bytesize=cfg["bytesize"],
            timeout=cfg["timeout"],
        )

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        self.client.close()

    def read(self, address, count=2):
        return self.client.read_holding_registers(
            address=address,
            count=count,
            device_id=self.device_id,
        )