"""Command: Reboot the device."""

from machine import reset


def execute(lcd, params, current_mode, log_func, chat_id=None):
    log_func("Rebooting device...")
    reset()
    return None
