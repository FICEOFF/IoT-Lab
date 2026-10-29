#include <SPI.h>
#include <RH_RF95.h>

RH_RF95 rf95;

float frequency = ; // Frequency Channel

void setup() {
    Serial.begin(9600);
    while (!Serial);
        Serial.println("Start Sketch");
    if (!rf95.init()) {
        Serial.println("init failed");
    }
    rf95.setFrequency(frequency);
    rf95.setSpreadingFactor(7);
    rf95.setSignalBandwidth(125000);
    rf95.setCodingRate4(5);
    rf95.setTxPower(13);
    Serial.print("Listening on frequency: ");
    Serial.println(frequency);
}

void loop() {
    if (rf95.available()) {
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
        if (rf95.recv(buf, &len)) {
            RH_RF95::printBuffer("request: ", buf, len);
            Serial.print("[REQUEST] ");
            Serial.println((char*)buf);
            Serial.print("RSSI: ");
            Serial.println(rf95.lastRssi(), DEC);
            uint8_t data[21] = "Hello LoRa Client";
            unsigned long startTime = micros();
            rf95.send(data, sizeof(data));
            rf95.waitPacketSent();
            unsigned long endTime = micros();
            unsigned long timeOnAir = endTime - startTime;
            Serial.print("Time on Air = ");
            Serial.print(timeOnAir / 1000.0);
            Serial.println(" ms");
            Serial.println("[REPLY] Sending to LoRa Client");
        }
        else {
            Serial.println("recv failed");
        }
    }
}
