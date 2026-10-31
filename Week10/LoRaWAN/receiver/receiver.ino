#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

static const u1_t PROGMEM APPEUI[8] = {  }; // Join EUI
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8); }

static const u1_t PROGMEM DEVEUI[8] = {  }; // Device EUI
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8); }

static const u1_t PROGMEM APPKEY[16] = {  }; // App Key
void os_getDevKey (u1_t* buf) { memcpy_P(buf, APPKEY, 16); }

#define LED_PIN 8
#define PWM_PIN 9

#define PWM_FOLLOWS_SWITCH 0

const unsigned TX_INTERVAL = 10;

static osjob_t sendjob;

const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 7,
    .dio = {2, 5, 6}
};

void applyOutputs(uint8_t sw, uint8_t pot) {
    digitalWrite(LED_PIN, sw ? HIGH : LOW);
    #if PWM_FOLLOWS_SWITCH
        analogWrite(PWM_PIN, sw ? pot : 0);
    #else
        analogWrite(PWM_PIN, pot);
    #endif
}

void do_send(osjob_t* j) {
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, not sending"));
        return;
    }
    uint8_t keepalive[1] = { 0 };
    LMIC_setTxData2(2, keepalive, sizeof(keepalive), 0);
    Serial.println(F("Keep-alive queued"));
}

void onEvent (ev_t ev) {
    Serial.print(os_getTime());
    Serial.print(": ");
    switch (ev) {
        case EV_JOINING:
            Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));
            LMIC_setLinkCheckMode(0);
            LMIC_setAdrMode(0);
            LMIC_setDrTxpow(DR_SF7, 14);
            break;
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_JOIN_TXCOMPLETE:
            Serial.println(F("EV_JOIN_TXCOMPLETE: no JoinAccept"));
            break;
        case EV_TXSTART:
            Serial.println(F("EV_TXSTART"));
            break;
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE"));
            if (LMIC.dataLen >= 2) {
                uint8_t sw  = LMIC.frame[LMIC.dataBeg];
                uint8_t pot = LMIC.frame[LMIC.dataBeg + 1];
                Serial.print(F("Downlink  sw="));
                Serial.print(sw);
                Serial.print(F("  pot="));
                Serial.println(pot);
                applyOutputs(sw, pot);
            } 
            else if (LMIC.dataLen > 0) {
                Serial.print(F("Unexpected downlink length: "));
                Serial.println(LMIC.dataLen);
            }
            os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
            break;
        case EV_RXSTART:
            break;
        default:
            Serial.print(F("Event: "));
            Serial.println((unsigned) ev);
            break;
    }
}

void setup() {
    Serial.begin(9600);
    Serial.println(F("Node B : LED Control"));
    pinMode(LED_PIN, OUTPUT);
    pinMode(PWM_PIN, OUTPUT);
    applyOutputs(0, 0);
    os_init();
    LMIC_reset();
    LMIC_setupChannel(0, 923200000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setLinkCheckMode(0);
    LMIC_setAdrMode(0);
    LMIC_setDrTxpow(DR_SF7, 14);
    do_send(&sendjob);
}

void loop() {
  os_runloop_once();
}
