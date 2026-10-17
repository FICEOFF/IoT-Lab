import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

OUT_PIN = 11
EN_PIN = 13

GPIO.setup(OUT_PIN, GPIO.IN)
GPIO.setup(EN_PIN, GPIO.OUT)

GPIO.output(EN_PIN, 1)

counter = 0
last_state = GPIO.input(OUT_PIN)

try:
    while True:
        detected = GPIO.input(OUT_PIN)
        if not detected and last_state:
            counter += 1
            print(f"[DETECTED] Count: {counter}")
        last_state = detected
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
