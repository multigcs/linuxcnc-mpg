// poe

#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>

uint8_t receiverAddress[] = {0x94, 0x3C, 0xC6, 0x33, 0x68, 0x98};
uint8_t myAddress[] = {0x30, 0xAE, 0xA4, 0x7B, 0x79, 0x90};



struct rx_data_t {
    float pos[6];
    int16_t ow_feed;
    int16_t ow_rapid;
    int16_t ow_spindle;
    int16_t leds;
};
const int rx_data_t_size = sizeof(rx_data_t);

union rx_Data_t{
    rx_data_t values;
    byte data[rx_data_t_size];
};
rx_Data_t rx_data;  

struct tx_data_t {
    int16_t jog;
    int16_t ow_feed;
    int16_t ow_rapid;
    int16_t ow_spindle;
    uint32_t buttons;
};
const int tx_data_t_size = sizeof(tx_data_t);

union tx_Data_t{
    tx_data_t values;
    byte data[tx_data_t_size];
};
tx_Data_t tx_data;  


esp_now_peer_info_t peerInfo;

void messageSent(const uint8_t *macAddr, esp_now_send_status_t status) {
    if (status == ESP_NOW_SEND_SUCCESS) {
    }
}

void messageReceived(const uint8_t* macAddr, const uint8_t* incomingData, int len) {
    memcpy(&tx_data.data, incomingData, sizeof(tx_data.data));
}

void setup() {
    Serial.begin(115200);
    // delay(1000); // uncomment if your serial monitor is empty
    WiFi.mode(WIFI_STA);
    esp_wifi_set_mac(WIFI_IF_STA, myAddress);


    if (esp_now_init() == ESP_OK) {
        //Serial.println("ESPNow Init success");
    } else {
        //Serial.println("ESPNow Init fail");
        return;
    }

    esp_now_register_send_cb(messageSent);
    esp_now_register_recv_cb(messageReceived);
    memcpy(peerInfo.peer_addr, receiverAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        //Serial.println("Failed to add peer");
        return;
    }
}

void loop() {
    uint8_t n = 0;
    uint8_t rx_buffer[rx_data_t_size];
    uint8_t tx_buffer[tx_data_t_size];
    uint8_t rlen = Serial.readBytes(rx_buffer, rx_data_t_size);
    if (rlen == rx_data_t_size) {
        for (n = 0; n < rx_data_t_size; n++) {
            rx_data.data[n] = rx_buffer[n];
        }
        esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &rx_data.data, sizeof(rx_data.data));
        if (result != ESP_OK) {
        }
        for (n = 0; n < tx_data_t_size; n++) {
            tx_buffer[n] = tx_data.data[n];
        }
        Serial.write(tx_buffer, tx_data_t_size);
    }
    while (Serial.available() > 0) {
        uint8_t c = Serial.read();
    }
    delay(5);
}

