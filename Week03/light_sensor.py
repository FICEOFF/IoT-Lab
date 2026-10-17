import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

LIGHT_PIN = 11

LED_PIN = 13

GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        if GPIO.input(LIGHT_PIN):
            GPIO.output(LED_PIN, 1)
            print("[DARK] LED: on")
        else:
            GPIO.output(LED_PIN, 0)
            print("[BRIGHT] LED: off")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
