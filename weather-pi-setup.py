#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import subprocess
import sys

# Add your specific directory to Python's search path
os.system("git clone https://github.com/pimoroni/weatherhat-python.git")
os.chdir("weatherhat-python")
os.system("sudo ./install.sh --unstable")
os.system("sudo pip3 install fonts font-manrope pyyaml adafruit-io numpy")
os.system("sudo raspi-config nonint do_i2c 0")
os.system("sudo raspi-config nonint do_spi 0")
os.system("sudo apt install python3-pip")
os.system("sudo apt-get install libatlas-base-dev")

os.system("sudo reboot")  