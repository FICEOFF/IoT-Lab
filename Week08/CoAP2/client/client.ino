#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <coap-simple.h>

const char WIFI_SSID[] = ""; // WiFi SSID
const char WIFI_PASSWORD[] = ""; // WiFi Password

IPAddress serverIP(10, 175, 4, 131); // Server IP Address
const uint16_t COAP_PORT = 5683;
const int POT_PIN = A0;

WiFiUDP udp;
Coap coap(udp);

unsigned long lastPoll = 0;
const unsigned long POLL_MS = 100;

void connectWiFi() {
    int status = WL_IDLE_STATUS;
    while (status != WL_CONNECTED) {
        status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        delay(10000);
    }
    Serial.print("WiFi IP Address: ");
    Serial.println(WiFi.localIP());
}

void onClientResponse(CoapPacket &packet, IPAddress ip, int port) {
    Serial.print("Response from "); Serial.println(ip);
    Serial.print("["); Serial.print(packet.code); Serial.print("] ");
    String payload;
    payload.reserve(packet.payloadlen);
    for (int i = 0; i < packet.payloadlen; i++) payload += (char)packet.payload[i];
    Serial.print("Response: "); Serial.println(payload);
}

void setup() {
    Serial.begin(115200);
    connectWiFi();
    udp.begin(0);
    coap.response(onClientResponse);
    coap.start();
    Serial.println("CoAP client ready.");
}

void loop() {
    coap.loop();
    if (millis() - lastPoll >= POLL_MS) {
        lastPoll = millis();
        float mapValue = map(analogRead(POT_PIN), 0, 1023, 0, 100);
        String payload = String(mapValue);
        coap.put(serverIP, 5683, "brightness", payload.c_str());
    }
}
