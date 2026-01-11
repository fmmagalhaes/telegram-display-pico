import time
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class CountdownMode(Mode):
    """Countdown display mode - shows countdown to a target date."""

    command_name = "countdown"
    needs_clear = True

    def validate_params(self, mode_params):
        """Validate countdown date parameter."""
        if not mode_params:
            return False, "Invalid date format. Use: /countdown YYYY-MM-DD"
        if not self._parse_date_static(mode_params):
            return False, "Invalid date format. Use: /countdown YYYY-MM-DD"
        return True, None

    @staticmethod
    def _parse_date_static(date_str):
        """
        Parse date string in YYYY-MM-DD format.

        Args:
            date_str: Date string in format YYYY-MM-DD

        Returns:
            Tuple of (year, month, day) or None if invalid
        """
        try:
            parts = date_str.split("-")
            if len(parts) != 3:
                return None

            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])

            # Basic validation
            if year < 2025 or year > 2100:
                return None
            if month < 1 or month > 12:
                return None
            if day < 1 or day > 31:
                return None

            return (year, month, day)
        except (ValueError, IndexError):
            return None

    def _date_to_timestamp(self, year, month, day):
        # mktime expects: (year, month, day, hour, minute, second, weekday, yearday)
        # weekday and yearday can be 0 as they're not used in the conversion
        return time.mktime((year, month, day, 0, 0, 0, 0, 0))

    def _calculate_countdown(self, target_date_str):
        """
        Calculate countdown to target date.

        Args:
            target_date_str: Date string in format YYYY-MM-DD

        Returns:
            Dict with countdown info or None if invalid
        """
        parsed = self._parse_date_static(target_date_str)
        if not parsed:
            return None

        year, month, day = parsed
        target_timestamp = self._date_to_timestamp(year, month, day)
        current_timestamp = time.time()

        diff_seconds = int(target_timestamp - current_timestamp)

        # Check if date is in the past
        if diff_seconds < 0:
            return {
                "days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 0,
                "is_past": True,
                "target_date": target_date_str
            }

        # Calculate components
        days = diff_seconds // 86400
        remaining = diff_seconds % 86400
        hours = remaining // 3600
        remaining = remaining % 3600
        minutes = remaining // 60
        seconds = remaining % 60

        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "is_past": False,
            "target_date": target_date_str
        }

    def display(self, lcd, log_func, mode_params):
        """
        Calculate and display countdown on LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function (not used)
            mode_params: Target date string in format YYYY-MM-DD
        """
        target_date_str = mode_params
        try:
            # Calculate countdown
            countdown_data = self._calculate_countdown(target_date_str)
            if not countdown_data:
                print(f"Invalid date format: {target_date_str}")
                return

            if countdown_data["is_past"]:
                message = f"Date has passed!\n{countdown_data['target_date']}"
                display_message(lcd, message, log_func)
            else:
                # Compact countdown format (e.g., "10d 05:12:30")
                countdown_str = f"{countdown_data['days']}d {countdown_data['hours']:02d}:{countdown_data['minutes']:02d}:{countdown_data['seconds']:02d}"
                message = f"Countdown to:\n{countdown_data['target_date']}\n\n{countdown_str}"
                display_message(lcd, message, log_func)

        except Exception as e:
            print(f"Error displaying countdown: {e}")
