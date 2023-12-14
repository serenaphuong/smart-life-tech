import RPi.GPIO as GPIO
import time
import serial

# Set up GPIO pins for touch sensing
touch_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]  # Adjust the number of pins as needed
GPIO.setmode(GPIO.BCM)
for pin in touch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up Serial communication
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Use '/dev/ttyS0' for Raspberry Pi 3

# Map sets of three characters to each sensor
sensor_mapping = {
    2: 'ABC',
    3: 'DEF',
    4: 'GHI',
    17: 'JKL',
    27: 'MNO',
    22: 'PQR',
    10: 'STU',
    9: 'VWX',
    11: 'YZ ',
    5: 'DEL',  # Delete button
    6: 'ENT',  # Enter button
    13: '   ',  # Space button (three spaces for clarity)
}

# Touch timing parameters
short_press_threshold = 1  # seconds for a short press
long_press_threshold = 2  # seconds for a long press

current_word = ""  # Variable to store the current word

def start_new_word():
    global current_word
    print("New word started")
    # Append the current word if space wasn't pressed
    if current_word and current_word[-1] != ' ':
        print(f"Appending current word: {current_word}")
        # Add your logic for appending the current word
        # For example, send the current word to a buffer or perform other actions
    current_word = ""  # Reset the current word

def cycle_characters(characters):
    global current_word
    print(f"Cycling characters: {characters}")
    
    # Find the index of the last character in the set
    index = characters.find(current_word[-1])

    # Cycle to the next character in the set
    next_char = characters[(index + 1) % len(characters)]

    # Append the cycled character to the current word
    current_word += next_char
    print(f"Current word: {current_word}")


try:
    while True:
        for pin in touch_pins:
            if GPIO.input(pin) == GPIO.LOW:
                start_time = time.time()
                characters = sensor_mapping.get(pin, '???')  # Default to '???' if no mapping found
                print(f"Touched on pin {pin}: {characters}")
                ser.write(f"Touched on pin {pin}: {characters}\n".encode())
                
                while GPIO.input(pin) == GPIO.LOW:
                    if time.time() - start_time > long_press_threshold:
                        start_new_word()
                        break
                    elif time.time() - start_time > short_press_threshold:
                        cycle_characters(characters)
                        time.sleep(0.5)  # Delay to avoid rapid consecutive touch events
                time.sleep(0.1)  # Debounce delay

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    ser.close()
