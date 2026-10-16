# Modbus Energy Gateway

A Python data-acquisition project for reading L&T WL4000 energy meters over an RS-485 Modbus RTU bus. The collector decodes meter registers and appends timestamped measurements to CSV for later analysis.

## Repository layout

- `collect.py` — polls the configured meter IDs and writes readings to `data/readings.csv`.
- `config/wl4000.json` — serial-port and Modbus connection settings.
- `modbus/` — serial client, register map, meter interface, and IEEE 754 decoder.
- `tests/` — small diagnostics for discovery, register reads, polling rate, and word order.
- `visualization.ipynb` — interactive plots from the collected CSV data.

## Hardware and configuration

You need an L&T WL4000 meter, an RS-485 adapter, and a machine with access to the serial port. Edit `config/wl4000.json` to match your port, baud rate, parity, and timeout. Update the meter IDs in `collect.py` for your bus.

On Linux, grant your user serial-device access (often through the `dialout` group) rather than running the collector as root.

## Install and run

```bash
git clone https://github.com/sparsh0106/modbus-energy-gateway.git
cd modbus-energy-gateway
python -m pip install pymodbus pandas plotly jupyter
python collect.py
```

Stop collection with `Ctrl+C`. To inspect or plot recorded data:

```bash
jupyter notebook visualization.ipynb
```

The meter model, register addresses, serial settings, and word order are hardware-specific. Verify them against your meter configuration before using the readings for operational decisions.
