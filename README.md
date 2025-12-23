# Tufty 2040

MicroPython projects for the [Pimoroni Tufty 2040](https://shop.pimoroni.com/products/tufty-2040) badge.

## Setup

1. Install [Pimoroni's MicroPython firmware](https://github.com/pimoroni/pimoroni-pico/releases) (look for `pimoroni-tufty2040-*.uf2`)
2. Flash by holding **BOOT** + tapping **PWR**, then copy the `.uf2` to the `RPI-RP2` drive, device will reboot automatically.

## Usage

```bash
# Copy file to device and reset
mpremote fs cp FILE.py :
mpremote soft-reset

# Remove file from device
mpremote fs rm :FILE.py
```
