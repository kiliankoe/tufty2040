from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import time

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)
display.set_backlight(0.7)

WIDTH, HEIGHT = display.get_bounds()

NAME = "kilko"
PRONOUNS = "he/him"

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

DROP_SHADOW_OFFSET = 4


def hsv_to_rgb(h, s, v):
    if s == 0.0:
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
    t = time.ticks_ms() / 1000.0

    for y in range(HEIGHT // GRID_SIZE + 1):
        for x in range(WIDTH // GRID_SIZE + 1):
            h = (x + y + int(t * 2)) / 50.0
            r, g, b = hsv_to_rgb(h, 0.5, 1)
            display.set_pen(display.create_pen(r, g, b))
            display.rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    display.set_font("bitmap8")

    display.set_pen(BLACK)
    display.text(NAME, name_x + DROP_SHADOW_OFFSET, name_y + DROP_SHADOW_OFFSET, WIDTH, name_size)
    display.set_pen(WHITE)
    display.text(NAME, name_x, name_y, WIDTH, name_size)

    display.set_pen(BLACK)
    display.text(PRONOUNS, pronouns_x + DROP_SHADOW_OFFSET, pronouns_y + DROP_SHADOW_OFFSET, WIDTH, pronouns_size)
    display.set_pen(WHITE)
    display.text(PRONOUNS, pronouns_x, pronouns_y, WIDTH, pronouns_size)

    display.update()
