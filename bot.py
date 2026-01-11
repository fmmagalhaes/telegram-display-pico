"""
Telegram LCD Display for Raspberry Pi Pico W

This bot listens for Telegram messages and displays content on an attached LCD screen.
It supports various display modes and commands to control the content shown.
"""

import time
from utils.mode_registry import get_command_to_mode
from utils.command_registry import get_system_commands
from utils.telegram_client import get_last_message
from utils.lcd_manager import display_message, get_lcd, clear_lcd
from utils.system_init import connect_wifi, init_time
from utils.log_utils import log
from utils.watchdog_decorator import with_watchdog
from config import POLL_INTERVAL, MODE_UPDATE_INTERVALS, DEFAULT_MODE

# Get registries
SYSTEM_COMMANDS = get_system_commands()
COMMAND_TO_MODE = get_command_to_mode()

# Global poll interval (can be overridden with /poll command)
poll_interval = POLL_INTERVAL

# Mode-specific update intervals (can be overridden with /interval command)
mode_update_intervals = MODE_UPDATE_INTERVALS.copy()


@with_watchdog
def _handle_mode_auto_update(lcd, mode, last_mode_update_time, mode_params=None):
    """Handle auto-update for modes that require periodic refreshes."""
    try:
        # Check if this mode has an update interval configured
        if mode not in mode_update_intervals:
            # No update interval configured for mode. Skipping auto-update.")
            return last_mode_update_time

        interval = mode_update_intervals[mode]
        current_time = time.time()

        # Check if it's time to update
        if (current_time - last_mode_update_time) < interval:
            return last_mode_update_time

        # Perform mode-specific update
        mode_class = COMMAND_TO_MODE.get(mode)
        if mode_class:
            mode_instance = mode_class()
            mode_instance.display(lcd, log, mode_params)
            return current_time

        return last_mode_update_time
    except Exception as e:
        log(f"Error in auto-update for mode {mode}: {e}")
        return last_mode_update_time


# Command handlers

def _handle_plain_text(lcd, message):
    display_message(lcd, message, log, word_wrap=True)
    return "message", None, 0


@with_watchdog
def _dispatch_system_command(lcd, current_mode, command, mode_params, chat_id):
    mode = SYSTEM_COMMANDS[command].execute(lcd, mode_params, current_mode, log, chat_id)
    return mode, None, 0


@with_watchdog
def _dispatch_mode_command(lcd, mode_class, mode_params=None):
    """
    Dispatch mode command with validation and proper display clearing.
    Returns: Tuple of (command_name, processed_params, last_update_time)
    """
    # Create instance once and reuse it
    mode_instance = mode_class()
    command_name = mode_instance.__class__.command_name

    # Let mode prepare/transform parameters
    mode_params = mode_instance.prepare_params(mode_params)

    # Validate parameters
    is_valid, error_msg = mode_instance.validate_params(mode_params)
    if not is_valid:
        log(error_msg)
        return None, None, 0

    # Clear display if needed
    if mode_instance.__class__.needs_clear:
        clear_lcd(lcd)

    # Log and display
    log_msg = f"Switched to {command_name} mode"
    if mode_params:
        log_msg += f": params = {mode_params}"
    log(log_msg)

    mode_instance.display(lcd, log, mode_params)
    return command_name, mode_params, time.time()


def _get_command(message):
    parts = message[1:].split(None, 1)
    command = parts[0]
    parameters = parts[1].strip().lower() if len(parts) > 1 else None
    return command, parameters


@with_watchdog
def _handle_command(lcd, message, current_mode=None, chat_id=None):
    """
    Handle incoming Telegram commands.
    Returns: Tuple of (mode, mode_params, last_update_time)
    """
    # Extract command and parameters
    if not message.startswith("/"):
        return _handle_plain_text(lcd, message)

    command, parameters = _get_command(message)

    # System commands such as /blink
    if command in SYSTEM_COMMANDS:
        return _dispatch_system_command(lcd, current_mode, command, parameters, chat_id)

    # Mode commands such as /weather
    mode_class = COMMAND_TO_MODE.get(command)
    if mode_class:
        return _dispatch_mode_command(lcd, mode_class, parameters)

    # Unknown command
    log(f"Unknown command: {message}")
    return None, None, 0


@with_watchdog
def _poll_messages(lcd, last_update_id, current_mode, mode_params, last_mode_update_time):
    """
    Poll Telegram for new messages and handle commands.
    Returns: Tuple of (new_update_id, current_mode, mode_params, last_mode_update_time)
    """
    try:
        print("\nPolling Telegram for new messages...")
        message, username, chat_id, new_update_id = get_last_message(last_update_id)

        if message:
            log(f"New message from {username}:\n{message}")
            try:
                new_mode, new_mode_params, update_time = _handle_command(lcd, message, current_mode, chat_id)

                if new_mode is not None:
                    current_mode = new_mode
                    mode_params = new_mode_params
                    last_mode_update_time = update_time
            except Exception as e:
                log(f"Error handling message: {e}")

        return new_update_id, current_mode, mode_params, last_mode_update_time

    except Exception as e:
        log(f"Error polling messages: {e}")
        return last_update_id, current_mode, mode_params, last_mode_update_time


def _main_loop(lcd):
    last_update_id = None
    current_mode = DEFAULT_MODE
    mode_params = None
    last_mode_update_time = 0
    last_poll_time = 0

    while True:
        try:
            # Handle mode auto-updates
            last_mode_update_time = _handle_mode_auto_update(lcd, current_mode, last_mode_update_time, mode_params)

            # Poll Telegram at poll_interval
            current_time = time.time()
            if (current_time - last_poll_time) >= poll_interval:
                last_update_id, current_mode, mode_params, last_mode_update_time = _poll_messages(
                    lcd, last_update_id, current_mode, mode_params, last_mode_update_time)
                last_poll_time = current_time

        except Exception as e:
            log(f"Error in main loop: {e}")

        # Small delay to prevent tight loop
        time.sleep(0.01)


@with_watchdog
def _start_bot():
    print("Starting LCD Display Bot...")
    lcd = get_lcd()
    display_message(lcd, "Pico started!\n\nConnecting to\nWiFi...", print)

    time.sleep(2)  # Small delay to ensure network interface is ready

    connected, ip = connect_wifi()
    if not connected:
        display_message(lcd, "Connection failed!", print)
        raise RuntimeError("WiFi connection failed")

    time.sleep(2)  # Give network time to stabilize before first remote call

    init_time()
    log("Bot started with IP: {}".format(ip))

    _main_loop(lcd)


def main():
    try:
        _start_bot()
    except KeyboardInterrupt:
        log("Bot stopped by user")
    except Exception as e:
        log(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
