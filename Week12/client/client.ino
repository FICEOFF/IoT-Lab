#include <WiFiS3.h>
#include <ArduinoMqttClient.h>
#include <Wire.h>
#include <Adafruit_SHT31.h>

const char* ssid = ""; // WiFi SSID
const char* password = ""; // WiFi Password

const char* broker = "mqtt-dashboard.com";
const int port = 1883;

const char* pubTopic = "67070164/temp";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
Adafruit_SHT31 sht31 = Adafruit_SHT31();

void connectWiFi() {
    Serial.print("Connecting to Wi-Fi...");
    while (WiFi.begin(ssid, password) != WL_CONNECTED) {
        Serial.print(".");
        delay(10000);
    }
    Serial.println("\n[CONNECTED] Wi-Fi connected");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}

void connectMQTT() {
    while (!mqttClient.connected()) {
        Serial.println("Connecting to MQTT broker...");
        mqttClient.setId("UNO-R4-WiFi-SHT31");
        if (mqttClient.connect(broker, port)) {
            Serial.println("[CONNECTED] MQTT broker connected");
        }
        else {
            Serial.print("[ERROR] MQTT connection failed: ");
            Serial.println(mqttClient.connectError());
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    Wire.begin();
    if (!sht31.begin(0x44)) {
        Serial.println("[ERROR] SHT31 sensor not found!");
        while (1) {
            delay(1000);
        }
    }
    Serial.println("[CONNECTED] SHT31 sensor detected");
    connectWiFi();
    connectMQTT();
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
    }
    if (!mqttClient.connected()) {
        connectMQTT();
    }
    mqttClient.poll();
    float temperature = sht31.readTemperature();
    if (!isnan(temperature)) {
        String message = String(temperature, 1);
        mqttClient.beginMessage(pubTopic, false, 1);
        mqttClient.print(message);
        if (mqttClient.endMessage() == 1) {
            Serial.print("[SENDING] Temperature: ");
            Serial.print(message);
            Serial.println(" °C");
        }
        else {
            Serial.println("[ERROR] Message publish failed");
        }
    }
    else {
        Serial.println("[ERROR] Failed to read SHT31 temperature");
    }
    delay(1000);
}
