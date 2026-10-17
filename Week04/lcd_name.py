from RPLCD.i2c import CharLCD
import time

lcd = CharLCD('PCF8574', 0x27)

def render_text(line1, line2):
    lcd.write_string(line1)
    lcd.crlf()
    lcd.write_string(line2)
    time.sleep(5)
    lcd.clear()

try:
    while True:
        render_text("Hello, Raspberry", "I2C LCD Ready!")
        render_text("Hello, Office", "ID is 67070164!")
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    lcd.clear()
