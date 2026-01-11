import time
from modes.base_mode import Mode, singleton
from utils.mode_registry import get_command_to_mode
from config import AUTO_MODE_SEQUENCE, AUTO_MODE_INTERVAL


@singleton
class AutoMode(Mode):
    """Auto display mode - cycles through different modes automatically."""

    command_name = "auto"
    needs_clear = True

    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.last_switch_time = 0
        self.mode_classes = get_command_to_mode()

    def display(self, lcd, log_func, mode_params=None):
        """
        Display the auto mode - cycles through configured modes.

        Args:
            lcd: LCD display object
            log_func: Logging function
            mode_params: Optional switch interval in seconds
        """
        sequence = AUTO_MODE_SEQUENCE
        switch_interval = (mode_params and int(mode_params)) or AUTO_MODE_INTERVAL

        if not sequence:
            log_func("Auto mode sequence is empty")
            return

        current_time = time.time()

        # Check if it's time to switch to the next mode
        if current_time - self.last_switch_time >= switch_interval:
            self.current_index = (self.current_index + 1) % len(sequence)
            self.last_switch_time = current_time

            # Get current mode configuration
            mode_config = sequence[self.current_index]
            mode_name = mode_config.get('mode', 'time')
            mode_params = mode_config.get('params', None)

            # Display the current mode
            mode_class = self.mode_classes.get(mode_name)
            if mode_class:
                try:
                    mode_instance = mode_class()
                    mode_instance.display(lcd, log_func, mode_params)
                except Exception as e:
                    log_func(f"Error displaying {mode_name} in auto mode: {e}")
            else:
                log_func(f"Unknown mode in auto sequence: {mode_name}")
        else:
            print("Auto mode: waiting to switch modes")
