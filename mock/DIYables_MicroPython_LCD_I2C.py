"""
Mock LCD I2C library for local testing
Prints LCD output to console instead of physical display
"""

class LCD_I2C:
    """Mock LCD I2C display that prints to console"""
    
    def __init__(self, i2c, addr, rows, cols):
        self.i2c = i2c
        self.addr = addr
        self.cols = cols
        self.rows = rows
        self.buffer = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.cursor_x = 0
        self.cursor_y = 0
        self._backlight_state = True
        print(f"[MOCK LCD] Initialized {cols}x{rows} LCD at address 0x{addr:02X}")
    
    def clear(self):
        """Clear the display"""
        self.buffer = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.cursor_x = 0
        self.cursor_y = 0
    
    def set_cursor(self, col, row):
        """Set cursor position"""
        self.cursor_x = col
        self.cursor_y = row
    
    def print(self, text):
        """Print text at current cursor position"""
        for char in str(text):
            if self.cursor_x < self.cols and self.cursor_y < self.rows:
                self.buffer[self.cursor_y][self.cursor_x] = char
                self.cursor_x += 1
        self._display_buffer()
    
    def backlight_on(self):
        """Turn backlight on"""
        self._backlight_state = True
        print("[MOCK LCD] Backlight ON")
    
    def backlight_off(self):
        """Turn backlight off"""
        self._backlight_state = False
        print("[MOCK LCD] Backlight OFF")
    
    def _display_buffer(self):
        """Display the buffer content in console - 20 cols x 4 rows"""
        border = "=" * (self.cols + 4)
        print(f"\n{border}")
        for row_idx in range(self.rows):
            line = ''.join(self.buffer[row_idx])
            print(f"| {line} |")
        print(f"{border}\n")
