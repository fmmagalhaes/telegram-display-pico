"""Command: Clear LCD display."""

from utils.lcd_manager import clear_lcd


def execute(lcd, params, current_mode, log_func, chat_id=None):
    clear_lcd(lcd)
    log_func("Display cleared")
    return "message"
