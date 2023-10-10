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

# Define the path to the other script
other_script_path = "weather.py"

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
font_size = 10
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

message = "Press A to start data collection. \nTurn off to stop data collection. \nPress X to display weather data for 30 seconds. \nPress Y to turn off screen and save battery."
size_x, size_y = draw.textsize(message, font)

# Calculate text position
x = (WIDTH - size_x) / 2
y = (HEIGHT / 2) - (size_y / 2)

# Draw background rectangle and write text.
draw.rectangle((0, 0, WIDTH, HEIGHT), back_colour)
draw.text((x, y), message, font=font, fill=text_colour)
disp.display(img)

# Keep running.
try:
    while True:
        pass

print("""buttons.py - Detect which button has been pressed
This example should demonstrate how to:
1. set up RPi.GPIO to read buttons,
2. determine which button has been pressed
Press Ctrl+C to exit!
""")

# The buttons on Weather HAT are connected to pins 5, 6, 16 and 24
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    if label == 'A':
        # Code to execute when button A is pressed
        # Adjust this value based on your needs
        # -17.5oC is an estimated error of having the HAT attached directly to the RPi that gets hot when turned on
        OFFSET = 0 # Note: this is an estimate, you may need to adjust this value based on your needs

        # Create a WeatherHat instance
        sensor = weatherhat.WeatherHAT() 

        # Create csv file for data collection
        file_path = '/home/pi/weatherdata.csv'

        # Check if the file already exists
        if not os.path.exists(file_path):
            # If not, create it and write the header
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Date','Time','Compensated Temperature','Uncompensated Temperature','Relative Humidity', 'Humidity', 'Pressure','Light (Lux)'])

        # Data collection loop
        try:
            while True:
                sensor.temperature_offset = OFFSET
                sensor.update(interval=60.0) # This can be adjusted (in seconds) to meet your needs. Note: you must also adjust the time.sleep on line 51
                timestamp = datetime.now()
                
                with open(file_path, mode="a", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([
                    timestamp.strftime("%Y-%m-%d"),
                        timestamp.strftime("%H:%M:%S"),
                        sensor.temperature,
                        sensor.device_temperature,
                        sensor.relative_humidity,
                        sensor.humidity,
                        sensor.pressure,
                        sensor.lux
                    ])

                time.sleep(60.0)

        # New canvas to draw on.
        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Text settings.
        font_size = 10
        font = ImageFont.truetype(UserFont, font_size)
        text_colour = (255, 255, 255)
        back_colour = (0, 170, 170)

        message = "Well done, data collection has started! \nTurn device off to stop recording. \nPress Y to turn off screen and save battery."
        size_x, size_y = draw.textsize(message, font)

        # Calculate text position
        x = (WIDTH - size_x) / 2
        y = (HEIGHT / 2) - (size_y / 2)

        # Draw background rectangle and write text.
        draw.rectangle((0, 0, WIDTH, HEIGHT), back_colour)
        draw.text((x, y), message, font=font, fill=text_colour)
        disp.display(img)

        # Keep running.
        try:
            while True:
                pass

        except KeyboardInterrupt:
            print("Data collection stopped.")
    elif label == 'B':
        # Code to execute when button B is pressed
        print("Button B pressed")
    elif label == 'X':
        # Code to execute when button X is pressed
        process = subprocess.Popen(["python3", other_script_path])
        # Wait for 30 seconds
        time.sleep(30)
        # Terminate the process after 30 seconds
        process.terminate()
    elif label == 'Y':
        # Code to execute when button Y is pressed
        # Turn off backlight on Press Y
        disp.set_backlight(0)

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 100ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=100)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()
