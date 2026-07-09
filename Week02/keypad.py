import RPi.GPIO as GPIO
import time

KEYPAD = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

GPIO.setmode(GPIO.BCM)

ROWS = [4, 17, 27, 22]
COLS = [5, 6, 13, 19]

RED_LIGHT = 16
GREEN_LIGHT = 20
BLUE_LIGHT = 21

for row_pin in ROWS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for col_pin in COLS:
    GPIO.setup(col_pin, GPIO.OUT)
    GPIO.output(col_pin, GPIO.HIGH)

GPIO.setup(RED_LIGHT, GPIO.OUT)
GPIO.setup(GREEN_LIGHT, GPIO.OUT)
GPIO.setup(BLUE_LIGHT, GPIO.OUT)

def get_key():
    key = None
    for col_num, col_pin in enumerate(COLS):
        GPIO.output(col_pin, GPIO.LOW)
        for row_num, row_pin in enumerate(ROWS):
            if GPIO.input(row_pin) == GPIO.LOW:
                key = KEYPAD[row_num][col_num]
                while GPIO.input(row_pin) == GPIO.LOW:
                    time.sleep(0.05)
        GPIO.output(col_pin, GPIO.HIGH)
    return key

def red_color():
    GPIO.output(RED_LIGHT, False)
    GPIO.output(GREEN_LIGHT, True)
    GPIO.output(BLUE_LIGHT, True)

def yellow_color():
    GPIO.output(RED_LIGHT, False)
    GPIO.output(GREEN_LIGHT, False)
    GPIO.output(BLUE_LIGHT, True)

def green_color():
    GPIO.output(RED_LIGHT, True)
    GPIO.output(GREEN_LIGHT, False)
    GPIO.output(BLUE_LIGHT, True)

def cyan_color():
    GPIO.output(RED_LIGHT, True)
    GPIO.output(GREEN_LIGHT, False)
    GPIO.output(BLUE_LIGHT, False)

def blue_color():
    GPIO.output(RED_LIGHT, True)
    GPIO.output(GREEN_LIGHT, True)
    GPIO.output(BLUE_LIGHT, False)

def magenta_color():
    GPIO.output(RED_LIGHT, False)
    GPIO.output(GREEN_LIGHT, True)
    GPIO.output(BLUE_LIGHT, False)

def white_color():
    GPIO.output(RED_LIGHT, False)
    GPIO.output(GREEN_LIGHT, False)
    GPIO.output(BLUE_LIGHT, False)

try:
    while True:
        pressed_key = get_key()
        if pressed_key is not None:
            print(f"Pressed: {pressed_key}")
            if pressed_key in [1, 'B', '#']:
                red_color()
            elif pressed_key in [2, 7, 'D']:
                yellow_color()
            elif pressed_key in [3, 8]:
                green_color()
            elif pressed_key in ['A', 9]:
                cyan_color()
            elif pressed_key in [4, 'C']:
                blue_color()
            elif pressed_key in [5, '*']:
                magenta_color()
            elif pressed_key in [6, 0]:
                white_color()
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
