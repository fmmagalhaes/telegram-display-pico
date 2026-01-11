from utils import system_init
from utils.telegram_client import send_telegram_message
from config import LOG_CHAT_ID


def log(message):
    """
    Log a message to console and to Telegram.
    """
    print(message)

    if system_init.wifi_connected:
        try:
            send_telegram_message(LOG_CHAT_ID, message)
        except Exception as e:
            print("Failed to send log message to Telegram:", e)
            pass  # Don't fail if logging to Telegram fails
