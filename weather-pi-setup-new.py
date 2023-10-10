#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import subprocess
import sys

# Add your specific directory to Python's search path
## if not os.path.exists("weatherhat-python"): # Once the code is finished I will add this back in
os.system("git clone https://github.com/DrRichBruce/PiLogger.git")
os.system("git clone https://github.com/pimoroni/weatherhat-python.git")
os.chdir("weatherhat-python")
os.system("./install.sh")
os.system("sudo pip3 install fonts font-manrope pyyaml adafruit-io numpy")
os.system("sudo raspi-config nonint do_i2c 0")
os.system("sudo raspi-config nonint do_spi 0")
os.system("sudo apt install python3-pip")
os.system("sudo apt-get install libatlas-base-dev")

# Define the crontab entry you want to add
new_cron_entry = "* * * * * @reboot python3 /home/pi/PiLogger/weather-pi-demo.py &"

# Use os.system to add the entry to the crontab
os.system(f'(crontab -l ; echo "{new_cron_entry}") | crontab -')

print("WeatherHAT Python library installed. System rebooting. Please close PuTTY and wait 15 seconds before reconnecting.")

os.system("sudo reboot")  