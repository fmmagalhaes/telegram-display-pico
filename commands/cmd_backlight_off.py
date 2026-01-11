"""Command: Turn LCD backlight off."""

from utils.lcd_manager import backlight_off


def execute(lcd, params, current_mode, log_func, chat_id=None):
    backlight_off(lcd)
    log_func("Backlight turned off. Press /on to turn it on.")
    return None
