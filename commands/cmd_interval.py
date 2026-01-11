"""Command: Set mode update interval."""


def execute(lcd, params, current_mode, log_func, chat_id=None):
    """Set the update interval for the current mode."""
    import bot
    
    interval = int(params)
    bot.mode_update_intervals[current_mode] = interval
    log_func(f"Update interval for {current_mode} mode set to {interval} seconds ({interval / 60:.2f} minutes)")
    return None
