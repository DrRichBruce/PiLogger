#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import subprocess
import sys

os.chdir("weatherhat-python/examples")

import weatherhat

# Adjust this value based on your needs
# -17.5oC is an estimated error of having the HAT attached directly to the RPi that gets hot when turned on
OFFSET = -17.5 # Note: this is an estimate, you may need to adjust this value based on your needs

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

print("Well done, data collection has started! Press CTRL+C or turn device off to stop recording.")

except KeyboardInterrupt:
    print("Data collection stopped.")
