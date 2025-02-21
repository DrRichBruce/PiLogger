#!/usr/bin/env python3

import os
import subprocess
import time

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
    eap=PEAP
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

import time
time.sleep(5)
os.system("sudo reboot")
