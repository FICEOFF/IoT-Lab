from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import logging, threading, time

GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 11
ECHO_PIN = 13

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

TUNNEL_URL = "" # Server tunnl.gg URL

logging.basicConfig(level=logging.INFO)

temperature = None
temp_lock = threading.Lock()

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="67070164-sub"
)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code:
        client.subscribe("67070164/temp")
        logging.info("[SUCCESS] MQTT connected")

def on_message(client, userdata, msg):
    global temperature
    with temp_lock:
        temperature = msg.payload.decode("utf-8")
        print(f"[RECEIVED] Message: {round(float(temperature), 1)}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("mqtt-dashboard.com", 1883, 60)
mqtt_client.loop_start()

mcp = MCPServer("RaspberryPi-IoT")

@mcp.tool()
def get_distance() -> str:
    GPIO.output(TRIG_PIN, 0)
    time.sleep(2)
    GPIO.output(TRIG_PIN, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, 0)
    while not GPIO.input(ECHO_PIN):
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN):
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150.0
    return f"Current distance: {round(float(distance), 1)} cm"

@mcp.tool()
def get_temperature() -> str:
    global temperature
    with temp_lock:
        temp = temperature
    if temp is None:
        return ("No temperature received yet.")
    return f"Current temperature: {round(float(temp), 1)} °C"

if __name__ == "__main__":
    try:
        security = TransportSecuritySettings(
            allowed_hosts=[
                f"{TUNNEL_URL}",
                f"{TUNNEL_URL}:*",
                "localhost:8000",
                "127.0.0.1:8000",
                "0.0.0.0:8000"
            ],
            allowed_origins=[
                f"https://{TUNNEL_URL}/"
            ]
        )
        mcp.run(
            transport="streamable-http",
            transport_security=security,
            host = "0.0.0.0"
        )
    except KeyboardInterrupt:
        print("\n[QUIT] Stopping program...")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        GPIO.cleanup()
