import machine
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class TemperatureMode(Mode):
    """Temperature display mode - shows Raspberry Pi Pico internal temperature."""

    command_name = "temp"
    needs_clear = False

    def _get_pico_temperature(self):
        """Read the internal temperature sensor."""
        try:
            # Read the internal temperature sensor
            sensor_temp = machine.ADC(4)
            reading = sensor_temp.read_u16() * (3.3 / 65535)
            # Convert voltage to temperature using Pico's datasheet formula:
            # T = 27 - (V_sense - 0.706V) / 0.001721V/°C
            # Where 27°C is reference temp, 0.706V is voltage at 27°C, and 0.001721 is temp coefficient
            temperature = 27 - (reading - 0.706) / 0.001721
            return temperature
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return None

    def display(self, lcd, log_func, mode_params=None):
        """
        Display Raspberry Pi Pico internal temperature on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
        """
        try:
            temp_c = self._get_pico_temperature()

            if temp_c is None:
                log_func("Failed to read temperature")
                return

            # Format the display message
            message = f"Pico temperature\n{temp_c:.1f} C"
            display_message(lcd, message, log_func)

            log_func(f"Temperature: {temp_c:.1f}C")

        except Exception as e:
            log_func(f"Error displaying temperature: {e}")
