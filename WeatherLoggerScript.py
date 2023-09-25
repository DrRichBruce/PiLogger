#!/usr/bin/env python3

import os
import time
from datetime import datetime
import csv
import subprocess
import weatherhat

def is_wifi_connected():
    result = os.popen("iwconfig wlan0").read()
    return "Not-Associated" not in result

def setup_eduroam():
    # Download the certificate
    os.system("sudo wget -O /usr/share/ca-certificates/uob-net-ca.crt https://www.wireless.bris.ac.uk/certs/eaproot/uob-net-ca.crt")
    os.system("sudo update-ca-certificates")

    # Ask the user for their eduroam credentials
    identity = input("Please enter your UoB username (e.g., ab12345@bristol.ac.uk): ")
    password = input("Please enter your UoB password: ")

    # Create the wpa_supplicant.conf content
    wpa_content = f'''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={{
    ssid="eduroam"
    key_mgmt=WPA-EAP
    auth_alg=OPEN
    eap=PEAP TTLS
    identity="{identity}"
    anonymous_identity="nobody@bristol.ac.uk"
    password="{password}"
    ca_cert="/usr/share/ca-certificates/uob-net-ca.crt"
    phase1="peaplabel=0"
    phase2="auth=MSCHAPV2"
    priority=999
    proactive_key_caching=1
}}
    '''

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
        f.write(wpa_content)

    # Restart the network and then reboot the Raspberry Pi
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    os.system("sudo reboot")

# Check for Internet connection. If there's no connection, attempt Eduroam setup
if os.system("ping -c 1 google.com") != 0:
    print("No internet connection detected.")
    choice = input("Would you like to set up Eduroam? (y/n): ").strip().lower()
    if choice == "y":
        setup_eduroam()
    else:
        print("You can manually set up a connection or use a mobile hotspot to provide internet.")
        exit()

# Constants for temperature correction
OFFSET = -17.5  # Adjust this value based on your needs

# Function to update the LCD with weather data
def update_lcd_with_weather_data():
    wh = weatherhat.WeatherHAT()
    
    wh.lcd.set_mode('dim')
    wh.lcd.set_brightness(100)
    wh.lcd.set_contrast(50)

    while True:
        wh.update()
        wh.lcd.clear()

        # Displaying compensated temperature
        if compensate_temperature == "y":
            corrected_temperature = wh.temperature + OFFSET
            wh.lcd.print('Temperature: {:.1f}C'.format(corrected_temperature))
        else:
            wh.lcd.print('Temperature: {:.1f}C'.format(wh.temperature))

        wh.lcd.print('Pressure: {:.1f}hPa'.format(wh.pressure))
        wh.lcd.print('Humidity: {:.1f}%'.format(wh.humidity))
        wh.lcd.show()
        time.sleep(10)


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

# Prompt the user for data collection interval
try:
    data_collection_interval = float(input("Enter Data Collection Interval (seconds, default: 60): "))
except ValueError:
    print("Invalid input for data collection interval. Using default interval of 60 seconds.")
    data_collection_interval = 60

# Prompt for LCD display setting
try:
    lcd_display = input("Enable LCD Display (y/n, default: y): ").strip().lower()
except TimeoutError:
    print("No input received for LCD display. Using default setting (y).")
    lcd_display = "y"

if lcd_display not in ["y", "n"]:
    print("Invalid input. LCD display disabled.")
    lcd_display = "n"

# Prompt for temperature compensation setting
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
    subprocess.run(['(crontab -l ; echo "' + cron_entry + '") | sort - | uniq - | crontab -'], shell=True)
    print("Crontab entry added to run the script at startup.")
except Exception as e:
    print("Failed to add crontab entry:", str(e))

# Data collection loop
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

        # Check if LCD display should be updated
        if lcd_display == "y":
            update_lcd_with_weather_data()

        time.sleep(data_collection_interval)

except KeyboardInterrupt:
    print("Data collection stopped.")
