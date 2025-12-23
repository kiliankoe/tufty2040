import time

import qrcode
from machine import ADC, Pin
from picographics import DISPLAY_TUFTY_2040, PEN_RGB332, PicoGraphics
from pimoroni import Button

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)

WIDTH, HEIGHT = display.get_bounds()

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

vbat_adc = ADC(Pin(29))
vref_adc = ADC(Pin(28))
vref_en = Pin(27, Pin.OUT)
vref_en.value(0)
usb_power = Pin(24, Pin.IN)

FULL_BATTERY = 3.7
EMPTY_BATTERY = 2.5

NAME = "kilko"
PRONOUNS = "he/him"
QR_URL = "https://kilian.io"

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
DARK_GRAY = display.create_pen(40, 40, 50)

DROP_SHADOW_OFFSET = 4

backlight = 0.7
display.set_backlight(backlight)

badge_mode = "badge"
show_battery = False

THEMES = [
    {"name": "Rainbow", "hue_min": 0.0, "hue_max": 1.0, "sat": 0.5, "val": 1.0},
    {"name": "Ocean", "hue_min": 0.5, "hue_max": 0.7, "sat": 0.6, "val": 1.0},
    {"name": "Sunset", "hue_min": 0.0, "hue_max": 0.15, "sat": 0.7, "val": 1.0},
    {"name": "Mono", "hue_min": 0.0, "hue_max": 0.0, "sat": 0.0, "val": 1.0},
    {"name": "Cyber", "hue_min": 0.75, "hue_max": 0.95, "sat": 0.8, "val": 1.0},
]
current_theme = 0


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v = int(v * 255)
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def get_battery_percent():
    vref_en.value(1)
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = (vbat_adc.read_u16() / 65535) * 3 * vdd
    vref_en.value(0)
    percentage = 100 * ((vbat - EMPTY_BATTERY) / (FULL_BATTERY - EMPTY_BATTERY))
    return max(0, min(100, percentage)), usb_power.value() == 1


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(WHITE)
    display.rectangle(ox, oy, size, size)
    display.set_pen(BLACK)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(
                    ox + x * module_size, oy + y * module_size, module_size, module_size
                )


def show_qr():
    display.set_pen(DARK_GRAY)
    display.clear()

    code = qrcode.QRCode()
    code.set_text(QR_URL)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)
    display.update()


name_size = 12
pronouns_size = 6

display.set_font("bitmap8")
name_width = display.measure_text(NAME, name_size)
name_x = (WIDTH - name_width) // 2
name_y = 60

pronouns_width = display.measure_text(PRONOUNS, pronouns_size)
pronouns_x = (WIDTH - pronouns_width) // 2
pronouns_y = 160

GRID_SIZE = 40

while True:
    if button_a.read():
        current_theme = (current_theme + 1) % len(THEMES)
        time.sleep(0.3)

    if button_b.read():
        show_battery = not show_battery
        time.sleep(0.3)

    if button_c.read():
        if badge_mode == "badge":
            badge_mode = "qr"
            show_qr()
        else:
            badge_mode = "badge"
        time.sleep(0.3)

    if button_up.read():
        backlight = min(1.0, backlight + 0.1)
        display.set_backlight(backlight)
        time.sleep(0.1)

    if button_down.read():
        backlight = max(0.1, backlight - 0.1)
        display.set_backlight(backlight)
        time.sleep(0.1)

    if badge_mode == "badge":
        t = time.ticks_ms() / 1000.0
        theme = THEMES[current_theme]

        for y in range(HEIGHT // GRID_SIZE + 1):
            for x in range(WIDTH // GRID_SIZE + 1):
                base_h = (x + y + int(t * 2)) / 50.0
                hue_range = theme["hue_max"] - theme["hue_min"]
                if hue_range > 0:
                    h = theme["hue_min"] + (base_h % 1.0) * hue_range
                else:
                    h = theme["hue_min"]
                    base_v = 0.5 + 0.5 * ((x + y + int(t * 2)) % 10) / 10.0
                    r, g, b = hsv_to_rgb(h, theme["sat"], base_v)
                    display.set_pen(display.create_pen(r, g, b))
                    display.rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    continue
                r, g, b = hsv_to_rgb(h, theme["sat"], theme["val"])
                display.set_pen(display.create_pen(r, g, b))
                display.rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

        display.set_font("bitmap8")

        display.set_pen(BLACK)
        display.text(
            NAME,
            name_x + DROP_SHADOW_OFFSET,
            name_y + DROP_SHADOW_OFFSET,
            WIDTH,
            name_size,
        )
        display.set_pen(WHITE)
        display.text(NAME, name_x, name_y, WIDTH, name_size)

        display.set_pen(BLACK)
        display.text(
            PRONOUNS,
            pronouns_x + DROP_SHADOW_OFFSET,
            pronouns_y + DROP_SHADOW_OFFSET,
            WIDTH,
            pronouns_size,
        )
        display.set_pen(WHITE)
        display.text(PRONOUNS, pronouns_x, pronouns_y, WIDTH, pronouns_size)

        if show_battery:
            percent, on_usb = get_battery_percent()
            if on_usb:
                battery_text = "USB"
            else:
                battery_text = "{:.0f}%".format(percent)
            display.set_pen(BLACK)
            display.text(battery_text, 12, HEIGHT - 28, WIDTH, 2)
            display.set_pen(WHITE)
            display.text(battery_text, 10, HEIGHT - 30, WIDTH, 2)

        display.update()
