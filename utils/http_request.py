"""
HTTP request helpers for MicroPython (urequests).
"""
import time
import urequests
from utils.watchdog_decorator import with_watchdog

REQUEST_TIMEOUT = 5  # seconds


def _extract_host(url):
    """Extract host from URL."""
    return url.split("://")[1].split("/")[0] if "://" in url else url.split("/")[0]


@with_watchdog
def http_post(url, data, timeout=REQUEST_TIMEOUT):
    start_time = time.time()
    response = urequests.post(url, json=data, timeout=timeout)
    response.close()
    elapsed_time = time.time() - start_time
    print(f"HTTP POST to {_extract_host(url)} completed (took {elapsed_time:.2f}s)")
    return response


@with_watchdog
def http_get_json(url, timeout=REQUEST_TIMEOUT):
    start_time = time.time()
    response = urequests.get(url, timeout=timeout)
    data = response.json()
    response.close()
    elapsed_time = time.time() - start_time
    print(f"HTTP GET to {_extract_host(url)} completed (took {elapsed_time:.2f}s)")
    return data
