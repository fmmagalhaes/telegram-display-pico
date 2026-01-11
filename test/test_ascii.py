"""
Test script for ASCII art mode
"""

import time
from modes.mode_ascii import AsciiArtMode, ASCII_ART
from utils.lcd_manager import get_lcd


def test_log(message):
    print(message)


def test_random_ascii():
    print("Testing random ASCII art...")
    lcd = get_lcd()
    mode = AsciiArtMode()
    mode.display(lcd, test_log, mode_params=None)
    print("Random ASCII art displayed successfully!")


def test_specific_ascii(art_name):
    print(f"Testing {art_name} ASCII art...")
    lcd = get_lcd()
    mode = AsciiArtMode()
    mode.display(lcd, test_log, mode_params=art_name)
    print(f"{art_name} ASCII art displayed successfully!")


def main():
    print("=== ASCII Art Mode Test ===\n")
    print(f"Testing all {len(ASCII_ART)} ASCII art designs...\n")

    lcd = get_lcd()
    mode = AsciiArtMode()

    # Iterate through all ASCII art with 3 second delay
    for art_name in ASCII_ART.keys():
        print(f"Displaying: {art_name}")
        mode.display(lcd, test_log, mode_params=art_name)
        time.sleep(3)

    print("\nAll ASCII art displayed!")


if __name__ == "__main__":
    main()
