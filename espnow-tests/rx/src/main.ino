// s2

#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>

uint8_t receiverAddress[] = {0x30, 0xAE, 0xA4, 0x7B, 0x79, 0x90};
uint8_t myAddress[] = {0x94, 0x3C, 0xC6, 0x33, 0x68, 0x98};





struct rx_data_t {
    float pos[6];
    int16_t ow_feed;
    int16_t ow_rapid;
    int16_t ow_spindle;
};
const int rx_data_t_size = sizeof(rx_data_t);

union rx_Data_t{
    rx_data_t values;
    byte data[rx_data_t_size];
};
rx_Data_t rx_data;  

struct tx_data_t {
    int32_t jog[6];
    int16_t ow_feed;
    int16_t ow_rapid;
    int16_t ow_spindle;
    uint16_t buttons;
};
const int tx_data_t_size = sizeof(tx_data_t);

union tx_Data_t{
    tx_data_t values;
    byte data[tx_data_t_size];
};
tx_Data_t tx_data;  





esp_now_peer_info_t peerInfo;
typedef struct messageToBeSent {
    char text[64];
    long runTime;
} messageToBeSent;

typedef struct receivedMessage {
    char text[64];
    int intVal;
    float floatVal;
} receivedMessage;

messageToBeSent myMessageToBeSent;

receivedMessage myReceivedMessage;

void messageReceived(const uint8_t* macAddr, const uint8_t* incomingData, int len) {
    memcpy(&rx_data.data, incomingData, sizeof(rx_data.data));

    Serial.printf("Incoming Message from: %02X:%02X:%02X:%02X:%02X:%02X \n\r", macAddr[0], macAddr[1], macAddr[2], macAddr[3], macAddr[4], macAddr[5]);

    Serial.println(rx_data.values.pos[0]);
    
    tx_data.values.jog[0] += 1;
    tx_data.values.jog[1] += 2;

    Serial.println();
    Serial.println("Sending answer...");
    Serial.println();

    esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &tx_data.data, sizeof(tx_data.data));
    if (result != ESP_OK) {
        Serial.println("Sending error");
    }
}

void setup() {
    Serial.begin(115200);
    // delay(1000); // uncomment if your serial monitor is empty
    WiFi.mode(WIFI_STA);
    esp_wifi_set_mac(WIFI_IF_STA, myAddress);

    if (esp_now_init() == ESP_OK) {
        Serial.println("ESPNow Init success");
    } else {
        Serial.println("ESPNow Init fail");
        return;
    }
    esp_now_register_recv_cb(messageReceived);

    memcpy(peerInfo.peer_addr, receiverAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
        return;
    }
}

void loop() {
}

