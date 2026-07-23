import RPi.GPIO as GPIO
import spidev
import time

X_CHANNEL = 0
Y_CHANNEL = 1
BUTTON_PIN = 22

RED_PIN = 11
GREEN_PIN = 13
BLUE_PIN = 15

CENTER_VALUE = 2048
DEADZONE = 100 

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

pwm_red = GPIO.PWM(RED_PIN, 2000)
pwm_green = GPIO.PWM(GREEN_PIN, 2000)
pwm_blue = GPIO.PWM(BLUE_PIN, 2000)

pwm_red.start(0)
pwm_green.start(0)
pwm_blue.start(0)

def ReadChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def map_value_to_pwm(value):
    return (value / 4095.0) * 100

last_button_state = 1
blue_on = False

try:
    while True:
        x_raw = ReadChannel(X_CHANNEL)
        y_raw = ReadChannel(Y_CHANNEL)
        red_duty = map_value_to_pwm(x_raw)
        green_duty = map_value_to_pwm(y_raw)
        pwm_red.ChangeDutyCycle(red_duty)
        pwm_green.ChangeDutyCycle(green_duty)
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == 0 and last_button_state == 1:
            blue_on = not blue_on
            time.sleep(0.05)
        last_button_state = button_state
        if blue_on:
            pwm_blue.ChangeDutyCycle(100)
        else:
            pwm_blue.ChangeDutyCycle(0)
        time.sleep(0.05)

except KeyboardInterrupt:
    pwm_red.stop()
    pwm_green.stop()
    pwm_blue.stop()
    spi.close()
    GPIO.cleanup()
