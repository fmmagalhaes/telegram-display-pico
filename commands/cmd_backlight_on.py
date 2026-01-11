"""Command: Turn LCD backlight on."""

from utils.lcd_manager import backlight_on


def execute(lcd, params, current_mode, log_func, chat_id=None):
    backlight_on(lcd)
    log_func("Backlight turned on. Press /off to turn it off.")
    return None
