"""
Mode Registry - Centralized registry for all display modes.
"""

# Cached command to mode mapping
_command_to_mode = None


def get_command_to_mode():
    """
    Get a dictionary mapping command names to mode classes.

    Returns:
        dict: {command_name: mode_class}
    """
    global _command_to_mode

    if _command_to_mode is None:
        # Import all mode classes (lazy load to avoid circular imports)
        from modes.mode_weather import WeatherMode
        from modes.mode_ascii import AsciiArtMode
        from modes.mode_countdown import CountdownMode
        from modes.mode_temperature import TemperatureMode
        from modes.mode_time import TimeMode
        from modes.mode_timer import TimerMode
        from modes.mode_auto import AutoMode
        from modes.mode_greetings import GreetingsMode
        from modes.mode_quotes import QuotesMode
        from modes.mode_daily import DailyMode
        from modes.mode_sentences import SentencesMode

        # List of all available mode classes
        modes = [
            WeatherMode,
            AsciiArtMode,
            CountdownMode,
            TimerMode,
            TimeMode,
            AutoMode,
            GreetingsMode,
            QuotesMode,
            DailyMode,
            TemperatureMode,
            SentencesMode,
        ]

        _command_to_mode = {}
        for mode_class in modes:
            instance = mode_class()
            _command_to_mode[instance.command_name] = mode_class

    return _command_to_mode
