from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
WIDTH, HEIGHT = display.get_bounds()

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
PURPLE = display.create_pen(128, 0, 128)

display.set_pen(PURPLE)
display.clear()

display.set_pen(WHITE)
display.set_font("bitmap8")
display.text("Hello, Tufty!", 10, 10, scale=4)
display.text("Ready to code!", 10, 60, scale=2)

display.update()
