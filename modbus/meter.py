from modbus.client import ModbusGateway
from modbus.decoder import FloatDecoder
from modbus.register_map import REGISTER_MAP


class WL4000:

    def __init__(self, word_order="low_high"):
        self.gateway = ModbusGateway()
        self.word_order = word_order

    def connect(self):
        return self.gateway.connect()

    def disconnect(self):
        self.gateway.disconnect()

    def read_parameter(self, name):
        reg = REGISTER_MAP[name]

        result = self.gateway.read(reg["address"], reg["length"])

        if result.isError():
            return {"value": None, "unit": reg["unit"], "error": str(result)}

        value = FloatDecoder.decode(result.registers, self.word_order)
        return {"value": value, "unit": reg["unit"], "error": None}

    def read_all(self):
        return {name: self.read_parameter(name) for name in REGISTER_MAP}