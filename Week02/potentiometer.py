import RPi.GPIO as GPIO
import spidev, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

LED_PIN = 11

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

GPIO.setup(LED_PIN, GPIO.OUT)

pi_pwm = GPIO.PWM(LED_PIN, 1000)
pi_pwm.start(0)

def readChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

try:
    while True:
        reading = readChannel(0)
        brightness = reading / 4095.0 * 100.0
        pi_pwm.ChangeDutyCycle(brightness)
        print(f"[{reading}] Brightness: {round(brightness)} %")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    pi_pwm.stop()
    spi.close()
    GPIO.cleanup()
