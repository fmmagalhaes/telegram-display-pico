from modes.base_mode import Mode
from utils.http_request import http_get_json
from utils.lcd_manager import display_message

URL = "http://192.168.1.250:3130/sentences"


class SentencesMode(Mode):
    """Sentences mode - fetches and displays sentences from an API."""

    command_name = "sentences"
    needs_clear = True

    def display(self, lcd, log_func, mode_params=None):
        """
        Display a sentence on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
        """
        try:
            data = http_get_json(URL)
            # Response format: {"sentence": "They looked up at the sky and saw a million stars."}
            sentence = data.get("sentence")
            display_message(lcd, sentence, log_func, word_wrap=True)
        except Exception as e:
            log_func(f"Sentences mode error: {e}")
