from DIYables_MicroPython_LCD_I2C import LCD_I2C
from machine import I2C, Pin
from config import LCD_I2C_ADDR, LCD_COLS, LCD_ROWS
from utils.lcd_manager import I2C_SCL_PIN, I2C_SDA_PIN

i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
print(i2c.scan())

lcd = LCD_I2C(i2c, LCD_I2C_ADDR, LCD_ROWS, LCD_COLS)
lcd.print("LCD Initialized")
print("LCD Initialized")
