"""
LCD Manager

Handles LCD display initialization, message formatting, and display operations.
"""

from machine import I2C, Pin
from DIYables_MicroPython_LCD_I2C import LCD_I2C
from config import LCD_I2C_ADDR, LCD_COLS, LCD_ROWS

# I2C pins (hardcoded - standard Pico pins)
I2C_SDA_PIN = 0
I2C_SCL_PIN = 1

# Global LCD instance
lcd = None


def _split_message(message, cols, rows, word_wrap):
    """Split message into lines that fit the LCD, preferring word boundaries and respecting newlines."""
    if not word_wrap:
        return _pad_lines(message.split('\n'), cols, rows)

    message = message.strip()
    lines = []
    remaining = message

    for _ in range(rows):
        if not remaining:
            lines.append("")
            continue

        # Check for explicit newline character
        newline_pos = remaining.find('\n')
        if newline_pos >= 0 and newline_pos < cols:
            # Newline found within the line width - break there
            lines.append(remaining[:newline_pos])
            remaining = remaining[newline_pos + 1:]
            continue

        if len(remaining) <= cols:
            lines.append(remaining)
            remaining = ""
            continue

        # Try to find a space to break on within the line width
        chunk = remaining[:cols]
        space_pos = chunk.rfind(' ')

        if space_pos > 0:
            # Found a space - break there
            lines.append(remaining[:space_pos])
            remaining = remaining[space_pos + 1:]
        else:
            # No space found - hard break at cols
            lines.append(chunk)
            remaining = remaining[cols:]

    # Pad lines to ensure LCD doesn't retain old characters
    return _pad_lines(lines, cols, rows)


def _pad_lines(lines, cols, rows):
    """
    Pad each line to cols width and ensure exactly rows lines are returned.
    This ensures the LCD does not retain old characters from previous messages.
    This is better than clearing the LCD each time, as it reduces flicker.
    Particularly important for modes that update frequently, like countdown.
    """
    result = []
    # Process existing lines
    for line in lines[:rows]:
        if len(line) < cols:
            line = line + " " * (cols - len(line))
        result.append(line[:cols])

    # Add empty lines to fill remaining rows
    while len(result) < rows:
        result.append(" " * cols)

    return result


def _remove_accents(text):
    ACCENTED_MAP = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ç': 'c',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U',
        'Ç': 'C'
    }
    return ''.join(ACCENTED_MAP.get(c, c) for c in text)


def display_message(lcd, message, log_func, word_wrap=False):
    try:
        if lcd is None:
            log_func(f"LCD not available, message: {message}")
            return
        message = _remove_accents(message)
        lines = _split_message(message, LCD_COLS, LCD_ROWS, word_wrap)
        for i, line in enumerate(lines):
            lcd.set_cursor(0, i)
            lcd.print(line)
        print("Successfully written to LCD")
    except Exception as e:
        log_func(f"Error displaying message: {e}")


def clear_lcd(lcd):
    if lcd is not None:
        lcd.clear()


def backlight_on(lcd):
    if lcd is not None:
        lcd.backlight_on()


def backlight_off(lcd):
    if lcd is not None:
        lcd.backlight_off()


def blink_lcd(lcd):
    # Note that the watchdog is set to 8 seconds
    import time
    if lcd is not None:
        for _ in range(5):
            time.sleep(0.5)
            backlight_off(lcd)
            time.sleep(0.5)
            backlight_on(lcd)


def get_lcd():
    """Get LCD display, initializing if needed. Returns LCD object or None if unavailable."""
    global lcd

    if lcd is not None:
        return lcd

    try:
        i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
        devices = i2c.scan()
        if not devices:
            print("No I2C devices found - running without LCD")
            return None

        print(f"I2C devices found: {[hex(d) for d in devices]}")
        lcd = LCD_I2C(i2c, LCD_I2C_ADDR, LCD_ROWS, LCD_COLS)
        # clear_lcd(lcd)
        # lcd.print("System ready")
        # lcd.set_cursor(0, 1)
        # lcd.print("Initializing...")
        return lcd
    except Exception as e:
        print(f"LCD init failed: {e} - running without LCD")
        return None
