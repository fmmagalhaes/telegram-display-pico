"""
Watchdog decorator utilities for automatic WDT feeding.
"""

from machine import WDT
import config

# Global watchdog timer instance (8s max for Pico)
if config.ENABLE_WATCHDOG:
    wdt = WDT(timeout=8388)
else:
    wdt = None


def with_watchdog(func):
    """
    Decorator that automatically feeds the global watchdog timer before and after function execution.
    Usage:
        @with_watchdog
        def my_function():
            ...
    """
    def wrapper(*args, **kwargs):
        if wdt:
            wdt.feed()
        try:
            return func(*args, **kwargs)
        finally:
            if wdt:
                wdt.feed()
    return wrapper
