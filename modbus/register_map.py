"""
WL4000 Register Map (corrected against L&T official memory map)

Addresses are ZERO-BASED for PyModbus (e.g. Modbus address 40141 -> 140 here).
"""

REGISTER_MAP = {
    "VRY":           {"address": 134, "length": 2, "unit": "V"},   # 40135
    "VYB":           {"address": 136, "length": 2, "unit": "V"},   # 40137
    "VBR":           {"address": 138, "length": 2, "unit": "V"},   # 40139
    "VLN_AVG":       {"address": 140, "length": 2, "unit": "V"},   # 40141
    "VR":            {"address": 142, "length": 2, "unit": "V"},   # 40143
    "VY":            {"address": 144, "length": 2, "unit": "V"},   # 40145
    "VB":            {"address": 146, "length": 2, "unit": "V"},   # 40147
    "CURRENT_TOTAL": {"address": 148, "length": 2, "unit": "A"},   # 40149
    "CURRENT_R":     {"address": 150, "length": 2, "unit": "A"},   # 40151
    "CURRENT_Y":     {"address": 152, "length": 2, "unit": "A"},   # 40153
    "CURRENT_B":     {"address": 154, "length": 2, "unit": "A"},   # 40155
    "FREQUENCY":     {"address": 156, "length": 2, "unit": "Hz"},  # 40157
    "WH_RECEIVED":   {"address": 158, "length": 2, "unit": "Wh"},  # 40159
    "VAH_RECEIVED":  {"address": 160, "length": 2, "unit": "VAh"}, # 40161
}