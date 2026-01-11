"""Command: Display help message."""


def execute(lcd, params, current_mode, log_func, chat_id=None):
    """Display help message with all available commands."""

    help_text = """Available commands:
/start - Show this help message
/help - Show this help message
/on - Turn backlight on
/off - Turn backlight off
/blink - Blink LCD backlight
/clear - Clear display
/temp - Show Pico temperature
/ascii - Show ASCII art
/greetings - Show greetings
/quotes - Show quotes
/weather [today|tomorrow] - Show weather
/time [m|s|ms] - Show time
/countdown YYYY-MM-DD - Countdown to date
/timer <minutes> - Start timer (default: 5 min)
/auto <seconds> - Auto cycle modes
/daily - Daily schedule mode
/poll <seconds> - Set poll interval
/interval <seconds> - Set mode update interval
/reboot - Reboot the device
<text> - Display custom message"""
    log_func(help_text)
    return None
