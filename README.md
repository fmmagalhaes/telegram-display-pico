# Telegram Display Pico

A Telegram bot that displays messages and useful information on a 20x4 I2C LCD using a Raspberry Pi Pico W.

## Hardware Required

- Raspberry Pi Pico W
- 20x4 I2C LCD display
- Jumper wires

## Setup

1. **Install MicroPython** - https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3

2. **Connect the LCD and install the DIYables_MicroPython_LCD_I2C library** - Follow this tutorial: https://newbiely.com/tutorials/raspberry-pico/raspberry-pi-pico-lcd-20x4

3. **Configure** - Copy `config.example.py` to `config.py` and add your credentials:
   ```python
   WIFI_SSID = "your_wifi"
   WIFI_PASSWORD = "your_password"
   BOT_TOKEN = "your_bot_token"  # Get from @BotFather on Telegram
   ```

4. **Upload files** - Copy all files to your Pico using MicroPico VS Code extension or similar

5. **Run** - Reset the Pico. It will connect to WiFi and start listening for Telegram commands!

### Testing Locally

To test the bot without the Pico hardware, use the `run_local.sh` script:
```bash
brew install micropython
./run_local.sh
```
This runs the bot with mock hardware modules for local development and testing.

## Features

Send messages to your bot to:
- Display custom messages
- Run commands that display specific content
- Auto-cycle through different display modes
- Configure update intervals and polling rates

## How It Works

1. Connects to WiFi on boot
2. Polls Telegram bot API for new messages
3. Processes commands and updates the LCD display
4. Supports multiple display modes with auto-refresh
5. Handles message wrapping for the 20x4 character display
6. Uses a hardware watchdog timer (8s timeout) to automatically restart on hangs 

## Extending

### Adding a New Display Mode

1. Create a new file in `modes/` (e.g., `mode_mymode.py`) inheriting from `Mode` base class
2. Set `command_name = "mymode"` and implement `display()` method
3. Add your mode to `MODES` list in `utils/mode_registry.py`
4. Add your mode to `MODE_UPDATE_INTERVALS` in `config.py`
5. Done! Use `/mymode` to activate it

### Adding a New System Command

1. Create a new file in `commands/` (e.g., `cmd_mycommand.py`) with an `execute()` function
2. Add your command as `"mycommand": cmd_mycommand` to `SYSTEM_COMMANDS` dict in `utils/command_registry.py`
3. Done! Use `/mycommand` to run it
