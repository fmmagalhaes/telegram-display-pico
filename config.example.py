# Configuration file for Telegram LCD Display
# Copy this file to config.py and edit the values for your setup

# WiFi credentials
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Telegram Bot Token (get from @BotFather on Telegram)
BOT_TOKEN = "your_bot_token_here"

# LCD Configuration
LCD_I2C_ADDR = 0x27  # Common addresses: 0x27 or 0x3F (use i2c.scan() to find yours)
LCD_COLS = 20
LCD_ROWS = 4

# Polling interval in seconds
POLL_INTERVAL = 5

# Watchdog timer configuration (8s max for Pico W)
# Set to True to enable automatic watchdog timer, False to disable
# This can cause the device to reset during debugging
ENABLE_WATCHDOG = False

# Telegram chat ID for logging
# Telegram bots are public, so anyone can send commands to them
# To prevent leaking information to the unknown users, the bot doesn't respond to the user who sent the command
# Instead, log messages will be sent to this chat ID (likely your own Telegram chat ID)
# Note that this doesn't restrict who can control the LCD. The bot will process commands from any user by design, but you can add your own authorization checks in the command handlers if needed.
LOG_CHAT_ID = 0

# Weather location
LATITUDE = 38.7223
LONGITUDE = -9.1393

# Default mode on startup
DEFAULT_MODE = "auto"

# Auto-update intervals (in seconds) for each mode
# This controls how often the display() method is called for each mode
MODE_UPDATE_INTERVALS = {
    "weather": 15 * 60,
    "ascii": 15 * 60,
    "greetings": 15 * 60,
    "quotes": 15 * 60,
    "temperature": 15 * 60,
    "sentences": 15 * 60,
    "daily": 60,
    "auto": 1,
    "timer": 1,
    "countdown": 1,
}

# Auto mode configuration
# Defines the sequence of modes to cycle through in auto mode
AUTO_MODE_SEQUENCE = [
    {"mode": "time"},
    {"mode": "weather"},
    {"mode": "weather", "params": "tomorrow"},
    {"mode": "ascii"},
    {"mode": "quotes"},
    {"mode": "temperature"},
]

# Time interval (in seconds) between mode switches in auto mode
AUTO_MODE_INTERVAL = 30

# Daily mode configuration
# Defines the schedule of modes based on time of day (24-hour format)
DAILY_MODE_SCHEDULE = [
    {"time": "08:00", "mode": "greetings"},
    {"time": "12:00", "mode": "weather"},
    {"time": "18:00", "mode": "quotes"},
    {"time": "21:00", "mode": "weather", "params": "tomorrow"},
    {"time": "22:00", "mode": "time"},
]
