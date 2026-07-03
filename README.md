# Powermeter Automation

A Python-based Modbus RTU data acquisition system for **L&T WL4000 series energy meters** over RS485. Polls 16 meters across a shared serial bus, decodes IEEE 754 float registers, and logs time-series data to CSV with interactive visualizations.

---

## Project Structure

```
Powermeter Automation/
├── config/
│   └── wl4000.json          # Serial port configuration
├── data/
│   ├── readings.csv         # Collected time-series data
│   ├── VLN_AVG.html         # Interactive voltage plot
│   ├── CURRENT_TOTAL.html   # Interactive current plot
│   └── FREQUENCY.html       # Interactive frequency plot
├── modbus/
│   ├── __init__.py
│   ├── client.py            # Modbus serial gateway
│   ├── decoder.py           # IEEE 754 float decoder
│   ├── meter.py             # High-level meter interface
│   └── register_map.py      # WL4000 register addresses
├── tests/
│   ├── check_modbus.py      # Raw register dump
│   ├── rate_test.py         # Polling speed benchmark
│   ├── read_all_test.py     # Full decoded read for one meter
│   ├── slave_discovery.py   # Scan bus for active meter IDs
│   └── word_order_test.py   # Diagnose float byte/word order
├── collect.py               # Main data collection loop
├── plot.py                  # Interactive Plotly visualizations
└── visualization.ipynb      # Exploratory analysis notebook
```

---

## Hardware

- **Meter**: L&T WL4000 LED / LCD Series Energy Meter
- **Interface**: RS485 Modbus RTU
- **Converter**: USB-to-RS485 adapter (`/dev/ttyACM0`)
- **Bus**: 16 meters, Slave IDs 1–12, 15–18

---

## Serial Configuration

`config/wl4000.json`:

```json
{
  "port": "/dev/ttyACM0",
  "baudrate": 9600,
  "parity": "E",
  "stopbits": 1,
  "bytesize": 8,
  "timeout": 2,
  "device_id": 1
}
```

Change `port` if your adapter appears on a different device path.

---

## Installation

```bash
git clone https://github.com/your-username/powermeter-automation.git
cd powermeter-automation
pip install pymodbus pandas plotly
```

---

## Usage

### 1. Discover active meters on the bus
```bash
sudo python3 tests/slave_discovery.py
```

### 2. Verify serial connection and raw registers
```bash
sudo python3 tests/check_modbus.py
```

### 3. Benchmark polling rate
```bash
sudo python3 tests/rate_test.py
```

### 4. Read all parameters from one meter
```bash
sudo python3 tests/read_all_test.py
```

### 5. Start data collection (all 16 meters, continuous)
```bash
sudo python3 collect.py
```
Appends one row per meter per sweep to `data/readings.csv`. Stop with `Ctrl+C`.

### 6. Generate interactive plots
```bash
python3 plot.py
```
Opens `data/VLN_AVG.html`, `data/CURRENT_TOTAL.html`, `data/FREQUENCY.html` in any browser. Hover over lines for exact values.

---

## Register Map

All registers are 32-bit IEEE 754 floats spanning 2 consecutive Modbus holding registers (word order: low word first).

| Parameter       | Modbus Address | Unit |
|----------------|---------------|------|
| VRY            | 40135         | V    |
| VYB            | 40137         | V    |
| VBR            | 40139         | V    |
| VLN_AVG        | 40141         | V    |
| VR             | 40143         | V    |
| VY             | 40145         | V    |
| VB             | 40147         | V    |
| CURRENT_TOTAL  | 40149         | A    |
| CURRENT_R      | 40151         | A    |
| CURRENT_Y      | 40153         | A    |
| CURRENT_B      | 40155         | A    |
| FREQUENCY      | 40157         | Hz   |
| WH_RECEIVED    | 40159         | Wh   |
| VAH_RECEIVED   | 40161         | VAh  |

---

## Data Format

`data/readings.csv` schema:

```
timestamp, meter_id, VRY, VYB, VBR, VLN_AVG, VR, VY, VB,
CURRENT_TOTAL, CURRENT_R, CURRENT_Y, CURRENT_B,
FREQUENCY, WH_RECEIVED, VAH_RECEIVED
```

Each sweep produces 16 rows (one per meter) with the same timestamp. Effective time resolution: **~6 minutes per full sweep** across all 16 meters at 9600 baud.

---

## How It Works

1. One shared `ModbusSerialClient` opens `/dev/ttyACM0` once.
2. For each meter ID, a single bulk Modbus read fetches all 28 registers (14 parameters × 2 registers each) in one request.
3. `FloatDecoder` walks the register list two at a time, swapping word order (`low_high`) and unpacking each pair as an IEEE 754 float via `struct`.
4. Results are collected into a list of dicts and appended to CSV in one write per sweep.

---

## Adapting to Your Setup

If you want to use this with your own meters, change the following:

**Different serial port**
Edit `config/wl4000.json` → `"port"`. On Windows use `"COM3"` etc., on Linux `/dev/ttyUSB0` is common for USB-RS485 adapters.

**Different baud rate or parity**
Edit `config/wl4000.json` → `"baudrate"` and `"parity"`. Match exactly what is programmed on your meters (check the meter's front panel programming menu).

**Different meter IDs**
Run `tests/slave_discovery.py` first — it scans IDs 1–247 and prints which ones respond. Then update `METER_IDS` in `collect.py` and `plot.py` with your found IDs.

**Different number of meters**
Just update `METER_IDS` in `collect.py` and `plot.py`. Everything else scales automatically.

**Different meter model / register addresses**
Edit `modbus/register_map.py`. Each entry needs:
```python
"PARAMETER_NAME": {"address": <zero-based address>, "length": 2, "unit": "V"}
```
Zero-based address = Modbus address − 1 (e.g. Modbus 40141 → address 140).

**Different word order**
Run `tests/word_order_test.py` — it tries all 4 byte/word order combinations and prints the decoded float for each. Pick the one that gives a sensible voltage reading (~220–240V for line-to-neutral). Then change `word_order="low_high"` to `word_order="high_low"` in `collect.py` and `tests/read_all_tests.py`.

**Different parameters to plot**
Edit `visualization.ipynb` → the list `["VLN_AVG", "CURRENT_TOTAL", "FREQUENCY"]` — replace with any column names from `readings.csv`.

---

## Notes

- Run with `sudo` on Linux to access `/dev/ttyACM0`, or add your user to the `dialout` group: `sudo usermod -aG dialout $USER`.
- Meter IDs 13 and 14 were not found on the bus during discovery.
- `WH_RECEIVED` reads zero on some meters — check CT polarity and reverse lock setting in the meter's programming menu.
- Word order is `low_high` (low register first) — confirmed via `tests/word_order_test.py`.
