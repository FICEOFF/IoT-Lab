import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

R_PIN = 11
G_PIN = 13
B_PIN = 15

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

GPIO.output(R_PIN, 1)
GPIO.output(G_PIN, 1)
GPIO.output(B_PIN, 1)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[RECEIVED] Message: {payload}")
    case1 = len(payload) == 2
    case2 = payload[0] in ("R", "G", "B")
    case3 = payload[1] in ("0", "1")
    if case1 and case2 and case3:
        color = payload[0]
        state = int(payload[1])
        match color:
            case "R":
                GPIO.output(R_PIN, state)
            case "G":
                GPIO.output(G_PIN, state)
            case "B":
                GPIO.output(B_PIN, state)

mqttc = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="67070164-sub",
    protocol=mqtt.MQTTv5
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

mqttc.subscribe("67070164/color", qos=1)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    GPIO.cleanup()
