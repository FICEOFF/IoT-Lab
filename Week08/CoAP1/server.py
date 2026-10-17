from aiocoap import resource, Context, Message
import aiocoap, asyncio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

LED_PIN = 12

GPIO.setup(LED_PIN, GPIO.OUT)

pi_pwm = GPIO.PWM(LED_PIN, 1000)
pi_pwm.start(0)

class LEDResource(resource.Resource):
    async def render_put(self, request):
        brightness = float(request.payload.decode())
        if 0 <= brightness <= 100:
            pi_pwm.ChangeDutyCycle(brightness)
            print(f"[{request.code} /brightness] Request: set to {round(brightness)} %")
        else:
            return Message(
                code=aiocoap.Code.BAD_REQUEST,
                payload=b"Must be between 0 and 100"
            )
        return Message(
            code=aiocoap.Code.CHANGED,
            payload=b"OK"
        )

async def main():
    root = resource.Site()
    root.add_resource(
        ["brightness"],
        LEDResource()
    )
    await Context.create_server_context(root, bind=("10.175.4.131", 5683)) # Server IP Address
    await asyncio.get_running_loop().create_future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    pi_pwm.stop()
    GPIO.cleanup()
