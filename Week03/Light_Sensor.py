import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

SENSOR = 16
LIGHT = 18

GPIO.setup(SENSOR, GPIO.IN)
GPIO.setup(LIGHT, GPIO.OUT)

while True:
    print(GPIO.input(SENSOR))
    if GPIO.input(SENSOR) == 0:
        GPIO.output(LIGHT, True)
    else:
        GPIO.output(LIGHT, False)
    time.sleep(0.1)
