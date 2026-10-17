import paho.mqtt.client as mqtt
import time

mqttc = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv5
)

mqttc.will_set(
    "67070164/lwt",
    payload="Publisher OFFLINE",
    qos=1,
    retain=True
)

mqttc.connect("mqtt-dashboard.com", 1883)

index = 1

try:
    while True:
        message = f"Hello from Publisher #{index}"
        mqttc.publish("67070164/pub", message, qos=1)
        print(f"[SENDING] {message}")
        index += 1
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
