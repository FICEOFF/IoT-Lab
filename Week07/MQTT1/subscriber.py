import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

LED_PIN = 11

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, 0)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[RECEIVED] Message: {payload}")
    if payload == "ON":
        GPIO.output(LED_PIN, 1)
    elif payload == "OFF":
        GPIO.output(LED_PIN, 0)

mqttc = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="67070164-sub",
    protocol=mqtt.MQTTv5
)

mqttc.will_set(
    "67070164/lwt",
    payload="Subscriber OFFLINE",
    qos=1,
    retain=True
)

mqttc.on_message = on_message

properties = mqtt.Properties(mqtt.PacketTypes.CONNECT)
properties.SessionExpiryInterval = 3600

mqttc.connect(
    "mqtt-dashboard.com",
    1883,
    clean_start=False,
    properties=properties
)

mqttc.subscribe("67070164/pub", qos=1)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
