import sys
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent))

from modbus.meter import WL4000

METER_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18]
FIELDS = [
    "VRY", "VYB", "VBR", "VLN_AVG",
    "VR", "VY", "VB",
    "CURRENT_TOTAL", "CURRENT_R", "CURRENT_Y", "CURRENT_B",
    "FREQUENCY", "WH_RECEIVED", "VAH_RECEIVED"
]

CSV_PATH = Path("data/readings.csv")
CSV_PATH.parent.mkdir(exist_ok=True)
write_header = not CSV_PATH.exists()

cycle = 0

try:
    while True:
        cycle += 1
        timestamp = datetime.now()
        print(f"\nCycle {cycle} | {timestamp.strftime('%H:%M:%S')}")

        rows = []
        for mid in METER_IDS:
            print(f"  Meter {mid}...", end=" ", flush=True)
            meter = WL4000(word_order="low_high")
            if not meter.connect():
                print("FAILED")
                continue
            try:
                result = meter.read_all()
                row = {"timestamp": timestamp, "meter_id": mid}
                row.update({f: result[f]["value"] for f in FIELDS})
                rows.append(row)
                print("OK")
            finally:
                meter.disconnect()

        if rows:
            sweep_df = pd.DataFrame(rows).set_index(["timestamp", "meter_id"])
            sweep_df.to_csv(CSV_PATH, mode="a", header=write_header)
            write_header = False
            print(f"Sweep saved. Rows this cycle: {len(rows)}")

except KeyboardInterrupt:
    print("\nStopped.")