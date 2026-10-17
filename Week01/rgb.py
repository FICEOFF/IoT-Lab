import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

R_PIN = 11
G_PIN = 13
B_PIN = 15

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

def set_rgb_color(r, g, b):
    GPIO.output(R_PIN, r)
    GPIO.output(G_PIN, g)
    GPIO.output(B_PIN, b)
    time.sleep(1)

try:
    while True:
        set_rgb_color(0, 1, 1)
        set_rgb_color(0, 0, 1)
        set_rgb_color(1, 0, 1)
        set_rgb_color(1, 0, 0)
        set_rgb_color(1, 1, 0)
        set_rgb_color(0, 1, 0)
        set_rgb_color(0, 0, 0)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
