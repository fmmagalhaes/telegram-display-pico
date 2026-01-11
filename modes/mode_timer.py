import time
from modes.base_mode import Mode, singleton
from utils.lcd_manager import display_message, backlight_off, blink_lcd


@singleton
class TimerMode(Mode):
    """Timer display mode - counts down minutes and alerts when complete."""

    command_name = "timer"
    needs_clear = True

    def __init__(self):
        super().__init__()
        self.is_timer_running = False
        self.start_message_shown = False

    def prepare_params(self, mode_params):
        """Convert minutes string to end_time timestamp."""
        import time
        minutes_str = mode_params or "5"
        try:
            minutes = int(minutes_str)
            end_time = time.time() + (minutes * 60)
            self.is_timer_running = True
            return end_time
        except (ValueError, TypeError):
            return None

    def validate_params(self, mode_params):
        if mode_params is None:
            return False, "Invalid timer duration. Use: /timer <minutes>"
        return True, None

    def _show_timer_start(self, lcd, log_func):
        """Display the timer start message and turn off backlight."""
        display_message(lcd, "Timer set!", log_func)
        log_func("Timer set!")
        time.sleep(2)
        backlight_off(lcd)

    def _show_timer_complete(self, lcd, log_func):
        """Display the timer completion message and flash backlight."""
        display_message(lcd, "Time is up!", log_func)
        log_func("Time is up!")
        blink_lcd(lcd)

    def display(self, lcd, log_func, mode_params):
        """
        Display the timer on LCD. When timer completes, shows message and flashes.

        Args:
            lcd: LCD display object
            log_func: Logging function (not used)
            mode_params: End time as Unix timestamp (float)
        """
        try:
            if not self.is_timer_running:
                return

            # Show start message only once when timer starts
            if not self.start_message_shown:
                self._show_timer_start(lcd, log_func)
                self.start_message_shown = True
                return

            backlight_off(lcd)

            end_time = mode_params
            current_time = time.time()

            if current_time >= end_time:
                self._show_timer_complete(lcd, log_func)

                # Timer is complete, stop running
                self.is_timer_running = False
                self.start_message_shown = False
            else:
                print(f"Timer running. Finishing in {int(end_time - current_time)} seconds...")  # type: ignore

        except Exception as e:
            print(f"Error displaying timer: {e}")
