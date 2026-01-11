"""Command: Set poll interval."""


def execute(lcd, params, current_mode, log_func, chat_id=None):
    """Set the Telegram polling interval."""
    import bot
    
    if params:
        bot.poll_interval = int(params)
        log_func(f"Poll interval set to {bot.poll_interval} seconds ({bot.poll_interval / 60:.2f} minutes)")
    else:
        log_func("Invalid poll command. Use: /poll <seconds>")
    
    return None
