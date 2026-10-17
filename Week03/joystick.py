import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

BUTTON_PIN = 12

R_PIN = 11
G_PIN = 13
B_PIN = 15

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

pwm_r = GPIO.PWM(R_PIN, 1000)
pwm_g = GPIO.PWM(G_PIN, 1000)
pwm_b = GPIO.PWM(B_PIN, 1000)

pwm_r.start(0)
pwm_g.start(0)
pwm_b.start(0)

def readChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def to_pwm(value):
    return (value / 4095.0) * 100.0

last_button_state = 1
g_on = 1

try:
    while True:
        x_raw = readChannel(0)
        y_raw = readChannel(1)
        pwm_r.ChangeDutyCycle(to_pwm(x_raw))
        pwm_b.ChangeDutyCycle(to_pwm(y_raw))
        button_state = GPIO.input(BUTTON_PIN)
        if button_state and not last_button_state:
            g_on = not g_on
            time.sleep(0.1)
        last_button_state = button_state
        if g_on:
            pwm_g.ChangeDutyCycle(100)
        else:
            pwm_g.ChangeDutyCycle(0)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    pwm_r.stop()
    pwm_g.stop()
    pwm_b.stop()
    spi.close()
    GPIO.cleanup()
