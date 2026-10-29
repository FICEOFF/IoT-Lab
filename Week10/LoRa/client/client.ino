#include <SPI.h>
#include <RH_RF95.h>

RH_RF95 rf95;

float frequency = ; // Frequency Channel

void setup() {
    Serial.begin(9600);
    Serial.println("Start LoRa Client");
    if (!rf95.init()) {
        Serial.println("init failed");
    }
    rf95.setFrequency(frequency);
    rf95.setTxPower(13);
    rf95.setSpreadingFactor(7);
    rf95.setSignalBandwidth(125000);
    rf95.setCodingRate4(5);
}

void loop() {
    Serial.println("[SENDING] Sending to LoRa Server");
    uint8_t data[50] = "Hello LoRa Server";
    unsigned long startTime = micros();
    rf95.send(data, sizeof(data));
    rf95.waitPacketSent();
    unsigned long endTime = micros();
    unsigned long timeOnAir = endTime - startTime;
    Serial.print("Time on Air = ");
    Serial.print(timeOnAir / 1000.0);
    Serial.println(" ms");
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf95.waitAvailableTimeout(3000)) {
        if (rf95.recv(buf, &len)) {
            Serial.print("[RECEIVE] ");
            Serial.println((char*)buf);
            Serial.print("RSSI: ");
            Serial.println(rf95.lastRssi(), DEC);
        }
        else {
            Serial.println("recv failed");
        }
    }
    else {
        Serial.println("No reply, is LoRa server running?");
    }
    delay(5000);
}
