from aiocoap import Context, Message
import aiocoap, asyncio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

SERVER_IP = "10.175.4.145" # Server IP Address
SERVER_PORT = 5683

LED_PIN = 12

GPIO.setup(LED_PIN, GPIO.OUT)

pi_pwm = GPIO.PWM(LED_PIN, 1000)
pi_pwm.start(0)

def set_led(response):
    brightness = float(response.payload.decode())
    print(f"[{response.code}] Response: set to {round(brightness)} %")
    pi_pwm.ChangeDutyCycle(float(brightness))

async def set_brightness():
    protocol = await Context.create_client_context()
    request = Message(
        code=aiocoap.Code.GET,
        uri=f"coap://{SERVER_IP}:{SERVER_PORT}/brightness"
    )
    request.opt.observe = 0
    requester = protocol.request(request)
    response = await requester.response
    set_led(response)
    async for response in requester.observation:
        set_led(response)

async def main():
    await set_brightness()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    pi_pwm.stop()
    GPIO.cleanup()
