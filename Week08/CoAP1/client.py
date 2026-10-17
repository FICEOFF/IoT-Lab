from aiocoap import Context, Message
import aiocoap, asyncio, random

SERVER_IP = "10.175.4.131" # Server IP Address
SERVER_PORT = 5683

async def set_brightness():
    protocol = await Context.create_client_context()
    request = Message(
        code=aiocoap.Code.PUT,
        uri=f"coap://{SERVER_IP}:{SERVER_PORT}/brightness",
        payload=f"{round(random.uniform(0, 100), 2)}".encode()
    )
    response = await protocol.request(request).response
    print(f"[{response.code}] Response: {response.payload.decode()}")

async def main():
    await set_brightness()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
