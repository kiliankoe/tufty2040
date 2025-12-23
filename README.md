# Tufty 2040

MicroPython projects for the [Pimoroni Tufty 2040](https://shop.pimoroni.com/products/tufty-2040).

## Setup

1. Install [Pimoroni's MicroPython firmware](https://github.com/pimoroni/pimoroni-pico/releases) (look for `pimoroni-tufty2040-*.uf2`)
2. Flash by holding **BOOT** + tapping **PWR**, then copy the `.uf2` to the `RPI-RP2` drive
3. Run `direnv allow` to activate the dev environment

## Usage

```bash
# List connected devices
mpremote connect list

# Open interactive REPL
mpremote repl

# Copy file to device
mpremote fs cp main.py :

# Copy multiple files
mpremote fs cp main.py :main.py + fs cp lib.py :lib.py

# List files on device
mpremote fs ls

# Run script without saving
mpremote run main.py

# Restart device
mpremote soft-reset

# Remove file from device
mpremote fs rm :main.py
```
