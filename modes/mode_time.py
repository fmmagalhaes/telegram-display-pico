import time
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class TimeMode(Mode):
    """Time display mode - shows current date and time."""

    command_name = "time"
    needs_clear = True

    def display(self, lcd, log_func, mode_params=None):
        """
        Display the current date and time on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function (not used)
            mode_params: Time format - "minute" (HH:MM), "second" (HH:MM:SS), or "millisecond" (HH:MM:SS.mmm)
        """
        format_mode = mode_params
        try:
            current_time = time.localtime()

            # Format date: YYYY-MM-DD
            date_str = "{:04d}-{:02d}-{:02d}".format(
                current_time[0],  # year
                current_time[1],  # month
                current_time[2]   # day
            )

            # Format time based on format_mode parameter
            if format_mode == "ms":
                # Get milliseconds
                ms = time.ticks_ms() % 1000
                # Format time: HH:MM:SS.mmm
                time_str = "{:02d}:{:02d}:{:02d}.{:03d}".format(
                    current_time[3],  # hour
                    current_time[4],  # minute
                    current_time[5],  # second
                    ms                # milliseconds
                )
            elif format_mode == "s":
                # Format time: HH:MM:SS
                time_str = "{:02d}:{:02d}:{:02d}".format(
                    current_time[3],  # hour
                    current_time[4],  # minute
                    current_time[5]   # second
                )
            else:  # minute (default)
                # Format time: HH:MM
                time_str = "{:02d}:{:02d}".format(
                    current_time[3],  # hour
                    current_time[4]   # minute
                )

            message = f"{date_str.center(20)}\n{time_str.center(20)}"
            display_message(lcd, message, log_func)

        except Exception as e:
            print(f"Error displaying time: {e}")
