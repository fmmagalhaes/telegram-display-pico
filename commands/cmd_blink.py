"""Command: Blink LCD backlight."""

from utils.lcd_manager import blink_lcd


def execute(lcd, params, current_mode, log_func, chat_id=None):
    log_func("Blinking LCD")
    blink_lcd(lcd)
    return None
