import spidev
import math
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

VCC = 3.3
RST = 10000
R0 = 10000
T0 = 298.15
B = 4050

def ReadChannel(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def adc_to_vol(adc):
    return adc / 4096 * VCC

def vol_to_rst(vol):
    return (RST * vol) / (VCC - vol)

def rst_to_tmp(rst):
    return (1 / ((1 / T0) + (1 / B) * math.log(rst / R0))) - 273.15

while True:
    reading = ReadChannel(0)
    vol = adc_to_vol(reading)
    rst = vol_to_rst(vol)
    tmp = rst_to_tmp(rst)
    print(f"Temp: {tmp:.2f}°C")
    time.sleep(1)
