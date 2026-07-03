import struct


class FloatDecoder:

    @staticmethod
    def decode(registers, word_order="high_low"):
        """
        Decode two 16-bit Modbus registers into a 32-bit float.

        word_order:
            "high_low" -> registers[0] is the high word (most common)
            "low_high" -> registers[0] is the low word
        """
        if len(registers) != 2:
            raise ValueError("Exactly two registers required.")

        first, second = registers

        if word_order == "high_low":
            high, low = first, second
        elif word_order == "low_high":
            high, low = second, first
        else:
            raise ValueError(f"Unknown word_order: {word_order}")

        packed = struct.pack(">HH", high, low)
        return struct.unpack(">f", packed)[0]

    @staticmethod
    def decode_all(registers, word_order="high_low"):
        """Decode a flat list of registers, two at a time, as floats."""
        values = {}
        for i in range(0, len(registers) - 1, 2):
            pair = registers[i:i + 2]
            values[f"value_{i // 2}"] = FloatDecoder.decode(pair, word_order)
        return values