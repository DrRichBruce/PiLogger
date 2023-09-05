#!/usr/bin/env python3

"""
RPi to environmental datalogger Python Script
Author: Dr Richard Bruce
Description: This script does XYZ.
"""
# If you haven't already you need to complete these steps before running this script:
# 1) Write RPI SD card using RPi imager app:
    # Hostname: bvspi(1-4) (.local)
    # Enable SHH: Use Password Authentication
    # Username: pi
    # Password: BVS2023
    # Configure wifi: Eduroam OR other local network
        
# 2) connect the RPi to the internet using your WiFi ID and password. For eduroam, follow these steps:
    # Connect to BristolWifiSetUp
    # Type this command to download the crt file and put it in the correct directory then update the certificates: 
        # sudo wget -O /usr/share/ca-certificates/uob-net-ca.crt https://www.wireless.bris.ac.uk/certs/eaproot/uob-net-ca.crt
        # sudo update-ca-certificates

    # Add the script below into the wpa applicant file without the #'s using the command: Sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
        # network={
            # ssid="eduroam"
            # key_mgmt=WPA-EAP
            # auth_alg=OPEN
            # eap=PEAP TTLS
            # identity="[insert your UoB username here]"
            # anonymous_identity="nobody@bristol.ac.uk"
            # password="[insert your UoB password here]"
            # ca_cert="/usr/share/ca-certificates/uob-net-ca.crt"
            # phase1="peaplabel=0"
            # phase2="auth=MSCHAPV2"
            # priority=999
            # proactive_key_caching=1

    # Reboot the device by typing the command:
        # sudo reboot

# 3) Download PuTTY to your laptop (not the RPi) to access the RPi remotely
    #Log in with yur host name and password
        # Host name: bvspi(1 - 4) [see label on RPi for number]
        # Password: BVS2023

# 4) Run this script to set up the RPi as an environmental data logger

# 5) Adjust your settings in the pop ups

# 6) Ensure you have the memory and battery life required to sustain the data logger for the required period of time

#ASK CHATGPT TO Enter line at the bottom of crontab that reads: @reboot python /home/pi/Pimoroni/weatherhat/examples/weather.py &

#MAIN SCRIPT to run RPi at environemtal data logger using the Pimoroni Weather HAT

#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import weatherhat
import subprocess

# Clone the weatherhat-python repository if it's not already installed
if not os.path.exists("weatherhat-python"):
    os.system("git clone https://github.com/pimoroni/weatherhat-python.git")
    os.chdir("weatherhat-python")
    os.system("./install.sh")
    os.chdir("..")

# Create a WeatherHat instance
sensor = weatherhat.WeatherHat()

# Specify the directory where the data will be saved
data_directory = "/home/pi/Documents/WeatherData"

# Ensure the directory exists, create it if not
os.makedirs(data_directory, exist_ok=True)

# Define the CSV file path
csv_file_path = os.path.join(data_directory, "weather_data.csv")

# Prompt the user for the data collection interval with a default of 60 seconds if no input is received within 10 seconds
try:
    data_collection_interval = float(input("Enter Data Collection Interval (seconds, default: 60): "))
except ValueError:
    print("Invalid input for data collection interval. Using default interval of 60 seconds.")
    data_collection_interval = 60

# Prompt the user to enable or disable the LCD display with a default of "y" (on) if no input is received within 10 seconds
try:
    lcd_display = input("Enable LCD Display (y/n, default: y): ").strip().lower()
except TimeoutError:
    print("No input received for LCD display. Using default setting (y).")
    lcd_display = "y"

if lcd_display not in ["y", "n"]:
    print("Invalid input. LCD display disabled.")
    lcd_display = "n"

# Prompt the user whether they want to compensate for temperature with a default of -17.5 if no input is received within 10 seconds
try:
    compensate_temperature = input("Compensate for temperature (y/n, default: n): ").strip().lower()
except TimeoutError:
    print("No input received for temperature compensation. Using default setting (n).")
    compensate_temperature = "n"

if compensate_temperature not in ["y", "n"]:
    print("Invalid input. Temperature compensation disabled.")
    compensate_temperature = "n"

# Add a crontab entry to run this script at startup
cron_entry = f'@reboot /usr/bin/python3 {os.path.abspath(__file__)}'

try:
    # Add the crontab entry
    subprocess.run(['(crontab -l ; echo "' + cron_entry + '") | sort - | uniq - | crontab -'], shell=True)
    print("Crontab entry added to run the script at startup.")
except Exception as e:
    print("Failed to add crontab entry:", str(e))

try:
    while True:
        sensor.update()

        timestamp = datetime.now()

        # Append data to the CSV file
        with open(csv_file_path, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                timestamp.strftime("%Y-%m-%d"),
                timestamp.strftime("%H:%M:%S"),
                sensor.temperature,
                sensor.device_temperature,
                sensor.relative_humidity,
                sensor.humidity,
                sensor.pressure,
                sensor.light_level
            ])

        print("Data saved at:", timestamp.strftime("%Y-%m-%d %H:%M:%S"))

        # Check if LCD display should be enabled
        if lcd_display == "y":
            # Add code here to update the LCD display

        time.sleep(data_collection_interval)
except KeyboardInterrupt:
    print("Data collection stopped.")
