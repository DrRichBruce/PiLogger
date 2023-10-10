#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import subprocess
import sys
import math
import pathlib

os.chdir("weatherhat-python/examples")

import signal
import RPi.GPIO as GPIO
import ST7789
import yaml
from fonts.ttf import ManropeBold as UserFont
from PIL import Image, ImageDraw, ImageFont

import weatherhat
from weatherhat import history

## Definitions
# Adjust this value based on your needs
# -17.5oC is an estimated error of having the HAT attached directly to the RPi that gets hot when turned on
OFFSET = 0 # Note: this is an estimate, you may need to adjust this value based on your needs

# Display settings
FPS = 10

SPI_SPEED_MHZ = 80

# Create LCD class instance.
disp = ST7789.ST7789(
    rotation=90,
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 15
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

message = "A: Record data. \nTurn off to stop. \nB: Display data (30 secs). \nY: Energy saving mode."
size_x, size_y = draw.textsize(message, font)

# Calculate text position
x = (WIDTH - size_x) / 2
y = (HEIGHT / 2) - (size_y / 2)

# Draw background rectangle and write text.
draw.rectangle((0, 0, WIDTH, HEIGHT), back_colour)
draw.text((x, y), message, font=font, fill=text_colour)
disp.display(img)

# The buttons on Weather HAT are connected to pins 5, 6, 16 and 24
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

