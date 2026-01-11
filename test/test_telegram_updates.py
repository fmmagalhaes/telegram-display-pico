"""
Simple test script for Telegram API calls with timeout
"""

from utils.telegram_client import get_last_message, send_telegram_message
from utils.system_init import connect_wifi
import time

print("Connecting to WiFi...")
connected, ip = connect_wifi()
if not connected:
    print("✗ WiFi connection failed")
    raise SystemExit(1)
print(f"✓ Connected with IP: {ip}")

print("\nTesting Telegram API with timeout...")
print("-" * 40)

# Test getting updates
print("\n1. Testing getUpdates API...")
count = 0
while True:
    count += 1
    print(f"  Attempt {count}...")
    message, username, chat_id, update_id = get_last_message(None)

    if message:
        print(f"✓ Success!")
        print(f"  Message: {message}")
        print(f"  From: {username}")
        print(f"  Chat ID: {chat_id}")
        print(f"  Update ID: {update_id}")
    else:
        print("✗ No messages received or timeout")

    time.sleep(0.5)
