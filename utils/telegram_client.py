from utils.http_request import http_post, http_get_json
from config import BOT_TOKEN

# Telegram API base URL
TELEGRAM_BOT_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_telegram_message(chat_id, text):
    try:
        print("Calling Telegram sendMessage API...")

        url = f"{TELEGRAM_BOT_API_URL}/sendMessage"
        data = {"chat_id": chat_id, "text": text}

        http_post(url, data)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


def get_last_message(last_update_id):
    """
    Fetch updates from Telegram and return the last text message.

    Returns: (message_text, username, chat_id, new_update_id)
    """
    print("Calling Telegram getUpdates API...")
    try:
        url = f"{TELEGRAM_BOT_API_URL}/getUpdates"
        if last_update_id:
            url += f"?offset={last_update_id + 1}"

        data = http_get_json(url)

        if not data or not data.get("ok") or not data.get("result"):
            return None, None, None, last_update_id

        updates = data["result"]
        if not updates:
            return None, None, None, last_update_id

        # Get the last update with a text message
        last_message = None
        last_username = None
        last_chat_id = None
        new_update_id = last_update_id

        for update in updates:
            new_update_id = update["update_id"]
            if "message" in update and "text" in update["message"]:
                last_message = update["message"]["text"]
                message_data = update["message"]
                from_user = message_data.get("from", {})
                first_name = from_user.get("first_name", "")
                last_name = from_user.get("last_name", "")
                last_username = f"{first_name} {last_name}".strip() or "Unknown"
                last_chat_id = from_user.get("id")

        return last_message, last_username, last_chat_id, new_update_id

    except Exception as e:
        print(f"Error fetching updates: {e}")
        return None, None, None, last_update_id
