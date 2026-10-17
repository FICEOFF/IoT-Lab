from RPLCD.i2c import CharLCD
import smbus3, time

bus = smbus3.SMBus(1)

lcd = CharLCD('PCF8574', 0x27)

try:
    while True:
        bus.i2c_wr(0x44,[0x2C,0x06])
        time.sleep(1)
        msg = bus.i2c_rd(0x44, 6)
        data = bytes(msg)
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
        lcd.clear()
        lcd.write_string(f"Temp: {cTemp:.2f} \xdfC")
        lcd.crlf()
        lcd.write_string(f"Humid: {humidity:.2f} %RH")
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    bus.close()
    lcd.clear()
