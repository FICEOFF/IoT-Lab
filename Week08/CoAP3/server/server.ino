#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <coap-simple.h>

const char WIFI_SSID[] = ""; // WiFi SSID
const char WIFI_PASSWORD[] = ""; // WiFi Password

const uint16_t COAP_PORT = 5683;
const int POT_PIN = A0;

WiFiUDP udp;
Coap coap(udp);

unsigned long lastPoll = 0;
const unsigned long POLL_MS = 100;
int lastSent = -1;

void connectWiFi() {
    int status = WL_IDLE_STATUS;
    while (status != WL_CONNECTED) {
        status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        delay(10000);
    }
    Serial.print("WiFi IP Address: ");
    Serial.println(WiFi.localIP());
}

void handleBrightness(CoapPacket &packet, IPAddress ip, int port) {
    float mapValue = map(analogRead(POT_PIN), 0, 1023, 0, 100);
    String payload = String(mapValue);
    int len = strlen(payload.c_str());
    uint32_t observeValue = 0;
    if (!packet.getObserveValue(observeValue)) {
        coap.sendResponse(ip, port, packet.messageid, payload.c_str(), len, COAP_CONTENT, COAP_TEXT_PLAIN, packet.token, packet.tokenlen);
        return;
    }
    if (observeValue == 0) {
        coap.addObserver("brightness", ip, port, packet.token, packet.tokenlen);
        coap.sendObserveResponse(ip, port, packet.messageid, payload.c_str(), len, COAP_CONTENT, COAP_TEXT_PLAIN, packet.token, packet.tokenlen, 0);
    }
    else if (observeValue == 1) {
        coap.removeObserver("brightness", ip, port, packet.token, packet.tokenlen);
        coap.sendResponse(ip, port, packet.messageid, payload.c_str(), len, COAP_CONTENT, COAP_TEXT_PLAIN, packet.token, packet.tokenlen);
    }
}

void setup() {
    Serial.begin(115200);
    connectWiFi();
    udp.begin(COAP_PORT);
    coap.server(handleBrightness, "brightness");
    coap.start();
    Serial.println("CoAP server ready @ udp/5683 resource: /brightness");
}

void loop() {
    coap.loop();
    if (millis() - lastPoll >= POLL_MS) {
        lastPoll = millis();
        float mapValue = map(analogRead(POT_PIN), 0, 1023, 0, 100);
        if (mapValue != lastSent) {
            lastSent = mapValue;
            String payload = String(mapValue);
            coap.notify("brightness", payload.c_str(), strlen(payload.c_str()), COAP_TEXT_PLAIN);
        }
    }
}
