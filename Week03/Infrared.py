import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

OUT = 16
EN = 18

GPIO.setup(OUT, GPIO.IN)
GPIO.setup(EN, GPIO.OUT)

GPIO.output(EN, GPIO.HIGH)

counter = 0
last_state = GPIO.input(OUT)

while True:
    current_state = GPIO.input(OUT)
    if last_state == 1 and current_state == 0:
        counter += 1
        print(counter)
    last_state = current_state
    time.sleep(0.05)
