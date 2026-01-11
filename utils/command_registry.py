"""
Command Registry - Centralized registry for system commands.
"""

from commands import (
    cmd_backlight_off,
    cmd_backlight_on,
    cmd_blink,
    cmd_clear,
    cmd_poll,
    cmd_interval,
    cmd_reboot,
    cmd_help
)

SYSTEM_COMMANDS = {
    "off": cmd_backlight_off,
    "on": cmd_backlight_on,
    "blink": cmd_blink,
    "clear": cmd_clear,
    "poll": cmd_poll,
    "interval": cmd_interval,
    "reboot": cmd_reboot,
    "help": cmd_help,
    "start": cmd_help,  # Alias for help
}


def get_system_commands():
    return SYSTEM_COMMANDS
