import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 11
ECHO_PIN = 13

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

try:
    while True:
        GPIO.output(TRIG_PIN, False)
        time.sleep(2)
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150.0
        print(f"[{pulse_duration}] Distance: {round(distance, 1)} cm")
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
