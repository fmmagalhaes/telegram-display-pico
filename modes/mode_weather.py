from utils.http_request import http_get_json
from config import LATITUDE, LONGITUDE
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class WeatherMode(Mode):
    """Weather display mode - shows current weather and forecast."""

    command_name = "weather"
    needs_clear = False

    def _weather_code_to_text(self, code):
        """Convert WMO weather code to short description."""
        codes = {
            0: "limpo", 1: "limpo", 2: "parcialmente nublado", 3: "nublado",
            45: "nevoeiro", 48: "nevoeiro",
            51: "chuvisco", 53: "chuvisco", 55: "chuvisco",
            61: "chuva", 63: "chuva", 65: "chuva",
            71: "neve", 73: "neve", 75: "neve",
            80: "aguaceiros", 81: "aguaceiros", 82: "aguaceiros",
            95: "trovoada", 96: "trovoada", 99: "trovoada"
        }
        return codes.get(code, None)

    def _get_weather_data(self, day_offset=0):
        """
        Fetch weather data from Open-Meteo API (no API key required).

        Args:
            day_offset: 0 for today, 1 for tomorrow

        Returns: dict with weather data or None on error
        """
        try:
            # Request 2 days of forecast to support tomorrow
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={LATITUDE}&longitude={LONGITUDE}"
                f"&current=temperature_2m,weather_code"
                f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
                f"&timezone=auto"
                f"&forecast_days=2"
            )

            data = http_get_json(url)

            if "current" not in data:
                return None

            # Get current temperature and weather
            current_temp = data["current"]["temperature_2m"]
            current_code = data["current"]["weather_code"]

            # Get daily max/min and overall weather for specified day
            daily_data = data["daily"]
            max_temp = daily_data["temperature_2m_max"][day_offset]
            min_temp = daily_data["temperature_2m_min"][day_offset]
            day_code = daily_data["weather_code"][day_offset]

            return {
                "current_temp": current_temp,
                "current_desc": self._weather_code_to_text(current_code),
                "max_temp": max_temp,
                "min_temp": min_temp,
                "day_desc": self._weather_code_to_text(day_code),
                "day_offset": day_offset
            }

        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None

    def display(self, lcd, log_func, mode_params=None):
        """
        Fetch and display weather data on LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
            mode_params: "tomorrow" to show tomorrow's forecast, else shows current weather
        """
        try:
            if mode_params == "tomorrow":
                day_offset = 1
                day_label = "Amanha"
            else:
                day_offset = 0
                day_label = "Hoje"

            # Fetch weather data
            weather_data = self._get_weather_data(day_offset)
            if not weather_data:
                log_func("Failed to fetch weather data")
                return

            # Build display lines
            if day_offset == 0:
                line1 = f"{day_label}: {weather_data['day_desc']}"
                line2 = f"Agora: {weather_data['current_temp']:.0f} C"  # ({weather_data['current_desc']})"
            else:
                line1 = f"{day_label}: {weather_data['day_desc']}"
                line2 = ""

            line3 = f"Max: {weather_data['max_temp']:.0f} C"
            line4 = f"Min: {weather_data['min_temp']:.0f} C"

            message = f"{line1}\n{line2}\n{line3}\n{line4}"
            display_message(lcd, message, log_func)

            print("Weather displayed on LCD")

        except Exception as e:
            log_func(f"Error displaying weather: {e}")
