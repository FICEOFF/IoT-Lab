import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)

red_ledpin = 8
green_ledpin = 10
blue_ledpin = 12

GPIO.setup(red_ledpin, GPIO.OUT)
GPIO.setup(green_ledpin, GPIO.OUT)
GPIO.setup(blue_ledpin, GPIO.OUT)

def red_color():
    GPIO.output(red_ledpin, False)
    GPIO.output(green_ledpin, True)
    GPIO.output(blue_ledpin, True)

def yellow_color():
    GPIO.output(red_ledpin, False)
    GPIO.output(green_ledpin, False)
    GPIO.output(blue_ledpin, True)

def green_color():
    GPIO.output(red_ledpin, True)
    GPIO.output(green_ledpin, False)
    GPIO.output(blue_ledpin, True)

def cyan_color():
    GPIO.output(red_ledpin, True)
    GPIO.output(green_ledpin, False)
    GPIO.output(blue_ledpin, False)

def blue_color():
    GPIO.output(red_ledpin, True)
    GPIO.output(green_ledpin, True)
    GPIO.output(blue_ledpin, False)

def magenta_color():
    GPIO.output(red_ledpin, False)
    GPIO.output(green_ledpin, True)
    GPIO.output(blue_ledpin, False)

def white_color():
    GPIO.output(red_ledpin, False)
    GPIO.output(green_ledpin, False)
    GPIO.output(blue_ledpin, False)

while True:
    for color in [red_color, yellow_color, green_color, cyan_color, blue_color, magenta_color, white_color]:
        color()
        time.sleep(1)
