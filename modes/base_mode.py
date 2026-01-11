"""
Base Mode class for all display modes.

All modes should inherit from this class and implement the display() method.
"""


def singleton(cls):
    """Singleton decorator to ensure only one instance of a class exists."""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


class Mode:
    """
    Base class for all display modes.

    Each mode must implement the display() method which receives:
    - lcd: LCD display object
    - log_func: Optional logging function
    - mode_params: Optional state data specific to the mode

    Class attributes for command handling:
    - command_name: The command string (without /) for this mode
    - needs_clear: Whether LCD should be cleared before switching to this mode
    """

    # Override these in subclasses
    command_name = None  # e.g., "weather", "time", "countdown"
    needs_clear = False  # Set to True if mode needs display cleared first

    def __init__(self):
        pass

    def prepare_params(self, mode_params):
        """
        Prepare and transform parameters before validation.
        Override this in subclasses that need parameter transformation.

        Args:
            mode_params: Raw parameters passed to the mode

        Returns:
            Transformed parameters ready for validation
        """
        return mode_params

    def validate_params(self, mode_params):
        """
        Validate parameters for this mode.

        Args:
            mode_params: Parameters passed to the mode

        Returns:
            Tuple of (is_valid: bool, error_message: str or None)
        """
        return True, None

    def display(self, lcd, log_func, mode_params=None):
        """
        Display the mode's content on the LCD.

        Args:
            lcd: LCD display object with methods like clear(), set_cursor(), print(), etc.
            log_func: Function for logging messages (e.g., to Telegram)
            mode_params: Optional state data for the mode (e.g., countdown date, time format)

        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement the display() method")
