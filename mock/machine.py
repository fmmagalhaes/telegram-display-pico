"""
Mock machine module for local testing without Pico hardware
"""

class Pin:
    """Mock Pin class"""
    def __init__(self, pin, mode=None):
        self.pin = pin
        self.mode = mode
        print(f"[MOCK] Pin {pin} initialized")

class I2C:
    """Mock I2C class"""
    def __init__(self, id, scl=None, sda=None, freq=None):
        self.id = id
        self.scl = scl
        self.sda = sda
        self.freq = freq
        print(f"[MOCK] I2C {id} initialized (SCL={scl}, SDA={sda}, freq={freq})")
    
    def scan(self):
        """Mock scan returning a fake I2C address"""
        return [0x27]  # Typical LCD I2C address
    
    def writeto(self, addr, buf):
        """Mock write"""
        pass
    
    def readfrom(self, addr, nbytes):
        """Mock read"""
        return b'\x00' * nbytes

class WDT:
    """Mock Watchdog Timer"""
    def __init__(self, timeout=None):
        self.timeout = timeout
        print(f"[MOCK] Watchdog timer initialized (timeout={timeout}ms)")
    
    def feed(self):
        """Mock watchdog feed"""
        pass

class ADC:
    """Mock Analog-to-Digital Converter"""
    def __init__(self, pin):
        self.pin = pin
        print(f"[MOCK] ADC initialized on pin {pin}")
    
    def read_u16(self):
        """Mock ADC read returning a value that simulates ~25°C"""
        # Using Pico's temperature formula: T = 27 - (V_sense - 0.706) / 0.001721
        # For ~25°C: V_sense = 0.706 + (27 - 25) * 0.001721 = 0.709442V
        # As 16-bit value: 0.709442 / 3.3 * 65535 = 14086
        return 14086

def reset():
    """Mock machine reset"""
    print("[MOCK] Machine reset requested")
    import sys
    sys.exit(0)
