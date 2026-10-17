import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

LED_PIN = 11

GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, 1)
        time.sleep(0.5)
        GPIO.output(LED_PIN, 0)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
