"""
System Initialization

Handles WiFi connection and system time initialization.
"""

import network
import time
from config import WIFI_SSID, WIFI_PASSWORD
from utils.watchdog_decorator import with_watchdog

# Track WiFi connection state for logging
wifi_connected = False


@with_watchdog
def connect_wifi():
    global wifi_connected
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    print(f"Connecting to {WIFI_SSID}...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            wifi_connected = True
            ip = wlan.ifconfig()[0]
            print(f"Connected! IP: {ip}")
            return True, ip
        max_wait -= 1
        time.sleep(1)

    print("WiFi connection failed!")
    return False, None


@with_watchdog
def init_time():
    # time() starts from a fixed epoch because there is no built-in real-time clock (RTC).
    # We use ntptime to set the correct time from an NTP server
    import ntptime
    print("Setting time from NTP server...")
    ntptime.settime()
