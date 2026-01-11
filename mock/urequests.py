"""
Mock urequests module for local testing
"""

import requests

# Wrap requests to match urequests API
get = requests.get
post = requests.post