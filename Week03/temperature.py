import spidev, math, time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

def readChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

try:
    while True:
        reading = readChannel(0)
        voltage = reading * 3.3 / 4095.0
        resistant = (voltage * 10000.0) / (3.3 - voltage)
        temperature = (298.15 * 4050.0) / (298.15 * math.log(resistant / 10000.0) + 4050.0) - 273.15
        print(f"[{reading}] Temperature: {round(temperature, 1)} °C")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    spi.close()
