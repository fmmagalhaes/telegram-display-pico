import time
from modes.base_mode import Mode, singleton
from utils.mode_registry import get_command_to_mode
from config import DAILY_MODE_SCHEDULE


@singleton
class DailyMode(Mode):
    """Daily display mode - shows different modes based on time of day schedule."""

    command_name = "daily"
    needs_clear = False

    def __init__(self):
        super().__init__()
        self.mode_classes = get_command_to_mode()

    def _get_current_schedule_item(self, schedule):
        """
        Get the current schedule item based on time of day.
        """
        if not schedule:
            return None

        # Get current time in minutes since midnight
        current_time = time.localtime()
        current_minutes = current_time[3] * 60 + current_time[4]

        # Convert schedule times to minutes and sort
        schedule_minutes = []
        for item in schedule:
            time_str = item.get('time', '00:00')
            try:
                time_parts = time_str.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                total_minutes = hour * 60 + minute
                schedule_minutes.append((total_minutes, item))
            except (ValueError, IndexError):
                continue

        # Sort by time
        schedule_minutes.sort(key=lambda x: x[0])

        # Find the appropriate schedule item
        # The schedule item is the one with the latest time that's <= current time
        selected_item = schedule_minutes[-1][1]  # Default to last item (wraps to next day)

        for minutes, item in schedule_minutes:
            if minutes <= current_minutes:
                selected_item = item
            else:
                break

        return selected_item

    def display(self, lcd, log_func, mode_params=None):
        """
        Display the daily mode - shows mode based on time schedule.

        Args:
            lcd: LCD display object
            log_func: Logging function
        """
        schedule = DAILY_MODE_SCHEDULE

        if not schedule:
            log_func("Daily mode schedule is empty")
            return

        # Get the current schedule item based on time
        schedule_item = self._get_current_schedule_item(schedule)

        if not schedule_item:
            log_func("No valid schedule item found")
            return

        mode_name = schedule_item.get('mode', 'time')
        mode_params = schedule_item.get('params', None)

        # Display the current mode
        mode_class = self.mode_classes.get(mode_name)
        if mode_class:
            try:
                mode_instance = mode_class()
                mode_instance.display(lcd, log_func, mode_params)
            except Exception as e:
                log_func(f"Error displaying {mode_name} in daily mode: {e}")
        else:
            log_func(f"Unknown mode in daily schedule: {mode_name}")
