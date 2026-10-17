import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

KEYPAD = [
    ["r", "y", "g", "c"],
    ["b", "m", "w", "r"],
    ["y", "g", "c", "b"],
    ["m", "w", "r", "y"]
]

ROWS = [12, 16, 18, 22]
COLS = [32, 36, 38, 40]

R_PIN = 11
G_PIN = 13
B_PIN = 15

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

for row_pin in ROWS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for col_pin in COLS:
    GPIO.setup(col_pin, GPIO.OUT)
    GPIO.output(col_pin, GPIO.HIGH)

def get_key():
    key = None
    for col_num, col_pin in enumerate(COLS):
        GPIO.output(col_pin, GPIO.LOW)
        for row_num, row_pin in enumerate(ROWS):
            if GPIO.input(row_pin) == GPIO.LOW:
                key = KEYPAD[row_num][col_num]
        GPIO.output(col_pin, GPIO.HIGH)
    return key

def set_rgb_color(r, g, b):
    GPIO.output(R_PIN, r)
    GPIO.output(G_PIN, g)
    GPIO.output(B_PIN, b)

try:
    while True:
        pressed_key = get_key()
        if pressed_key is not None:
            match pressed_key:
                case "r":
                    set_rgb_color(0, 1, 1)
                case "y":
                    set_rgb_color(0, 0, 1)
                case "g":
                    set_rgb_color(1, 0, 1)
                case "c":
                    set_rgb_color(1, 0, 0)
                case "b":
                    set_rgb_color(1, 1, 0)
                case "m":
                    set_rgb_color(0, 1, 0)
                case "w":
                    set_rgb_color(0, 0, 0)
        else:
            set_rgb_color(1, 1, 1)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
