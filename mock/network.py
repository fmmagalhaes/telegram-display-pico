"""
Mock network module for local testing
"""

STA_IF = 1
AP_IF = 0

class WLAN:
    """Mock WLAN class"""
    def __init__(self, interface_id):
        self.interface_id = interface_id
        self._active = False
        self._connected = False
        print(f"[MOCK] WLAN initialized (interface={interface_id})")
    
    def active(self, state=None):
        """Get or set active state"""
        if state is not None:
            self._active = state
            print(f"[MOCK] WLAN active = {state}")
        return self._active
    
    def connect(self, ssid, password):
        """Mock WiFi connection"""
        print(f"[MOCK] Connecting to WiFi: {ssid}")
        self._connected = True
    
    def isconnected(self):
        """Check if connected"""
        return self._connected
    
    def ifconfig(self):
        """Return mock network config"""
        return ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
