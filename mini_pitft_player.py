# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""
import digitalio
import board
from animatedgif import AnimatedGif
import numpy  # pylint: disable=unused-import
from adafruit_seesaw import seesaw, rotaryio, digitalio as ss_digitalio  # pylint: disable=unused-import
from adafruit_rgb_display import st7789
from gpiozero import RotaryEncoder, PWMLED


# i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# seesaw = seesaw.Seesaw(i2c, addr=0x36)

# seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
# print("Found product {}".format(seesaw_product))
# if seesaw_product != 4991:
#     print("Wrong firmware loaded? Make sure you have a rotary encoder connected.")

# seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
# button = ss_digitalio.DigitalIO(seesaw, 24)
# encoder = rotaryio.IncrementalEncoder(seesaw)
encoder = RotaryEncoder(12, 16, wrap=False, max_steps=24)

# Change to match your display
BUTTON_UP = board.D23
BUTTON_DOWN = board.D24

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)


def init_button(pin):
    digital_button = digitalio.DigitalInOut(pin)
    digital_button.switch_to_input(pull=digitalio.Pull.UP)
    return digital_button


class TFTAnimatedGif(AnimatedGif):
    def __init__(self, display, include_delays=True, folder=None):
        self._width = display.width
        self._height = display.height
        self.up_button = init_button(BUTTON_UP)
        self.down_button = init_button(BUTTON_DOWN)
        self._last_position = None
        self._button_state = False
        super().__init__(display, include_delays=include_delays, folder=folder)

    def get_next_value(self):
        position = encoder.value
        if position != self._last_position:
            self._last_position = position
        return str(position)

    def update_display(self, image):
        self.display.image(image)


# Config for display baudrate (default max is 64mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=None,
    baudrate=BAUDRATE,
)

gif_player = TFTAnimatedGif(disp, include_delays=False, folder="images")
