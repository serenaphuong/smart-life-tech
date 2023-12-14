import board
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C #pip install adafruit-circuitpython-charlcd

import time

# Set up LCD
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Display a message on the LCD
lcd.message = "LCD Test\nHello, World!"

# Wait for a few seconds
time.sleep(5)

# Clear the LCD
lcd.clear()
