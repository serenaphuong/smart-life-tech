import time
import RPi.GPIO as GPIO
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

# Set up GPIO pins for touch sensing
touch_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]  # Adjust the number of pins as needed
GPIO.setmode(GPIO.BCM)
for pin in touch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up LCD
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Map pairs of alphabets to each sensor
alphabet_mapping = {
    2: ['A', 'B'],
    3: ['C', 'D'],
    4: ['E', 'F'],
    17: ['G', 'H'],
    27: ['I', 'J'],
    22: ['K', 'L'],
    10: ['M', 'N'],
    9: ['O', 'P'],
    11: ['Q', 'R'],
    5: ['S', 'T'],
    6: ['U', 'V'],
    13: ['W', 'X'],
    19: ['Y', 'Z'],
    26: [' ', ' ']  # Double space sensor
}

# Function to handle touch events
def handle_touch():
    pressed_chars = ""
    timeout_duration = 2  # Set the timeout duration in seconds
    last_touch_time = time.time()

    while True:
        for pin in touch_pins:
            if GPIO.input(pin) == GPIO.LOW:
                # Convert touch event to alphabet based on the mapping
                alphabet_pair = alphabet_mapping.get(pin)
                if alphabet_pair:
                    pressed_chars += alphabet_pair[0]
                    lcd.clear()
                    lcd.message = f"Pressed: {alphabet_pair[0]}"
                    time.sleep(1)  # Avoid rapid consecutive touch events
                    pressed_chars += alphabet_pair[1]
                    lcd.clear()
                    lcd.message = f"Pressed: {alphabet_pair[1]}"
                    time.sleep(1)  # Avoid rapid consecutive touch events
                    last_touch_time = time.time()  # Update the last touch time
                else:
                    lcd.clear()
                    lcd.message = "Invalid sensor"
        
        # Check for timeout
        if time.time() - last_touch_time > timeout_duration and pressed_chars:
            lcd.clear()
            lcd.message = f"Word: {pressed_chars}"
            time.sleep(1)  # Add a delay before resetting pressed_chars
            pressed_chars = ""

# Main loop
try:
    handle_touch()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    GPIO.cleanup()
