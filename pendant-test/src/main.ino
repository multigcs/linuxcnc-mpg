
#include <Wire.h> 
#include <ESPRotary.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>


#define ADC 14
#define TFT_DC 33
#define TFT_CS 34
#define CLICKS_PER_STEP 4
#define PSTEP 32

SPIClass fspi = SPIClass(FSPI);
Adafruit_ILI9341 tft = Adafruit_ILI9341(&fspi, TFT_DC, TFT_CS);

ESPRotary r1;
ESPRotary r2;
ESPRotary r3;
ESPRotary r4;

uint8_t receiverAddress[] = {0x30, 0xAE, 0xA4, 0x7B, 0x79, 0x90};
uint8_t myAddress[] = {0x94, 0x3C, 0xC6, 0x33, 0x68, 0x98};
esp_now_peer_info_t peerInfo;

hw_timer_t *timer = NULL;

int col_pins[6] = {10, 8, 6, 4, 2, 1};
int row_pins[4] = {7, 9, 5, 11};



uint8_t sw_stat[3][6] = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
};

int32_t enc_diff[4] = {0, 0, 0, 0};

uint8_t overwrite_feed = 0;
char tmp_str[100];

struct rx_data_t {
    float pos[6];
    int16_t ow_feed;
    int16_t ow_rapid;
    int16_t ow_spindle;
    uint16_t leds;
    float jog_scale;
    float aux1;
    float aux2;
};
const int rx_data_t_size = sizeof(rx_data_t);

rx_data_t last_values;
float last_batt_voltage = -1.0;



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


uint8_t rx_counter = 0;
uint8_t update = 0;

void IRAM_ATTR handleLoop() {
    r1.loop();
    r2.loop();
    r3.loop();
    r4.loop();
}


void messageReceived(const uint8_t* macAddr, const uint8_t* incomingData, int len) {
    memcpy(&rx_data.data, incomingData, sizeof(rx_data.data));

    rx_counter++;

    esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &tx_data.data, sizeof(tx_data.data));
    if (result != ESP_OK) {
    }
}


void setup() {
    uint8_t n = 0;
    Serial.begin(115200);
    Serial.setTimeout(10);

    for (n = 0; n < 6; n++) {
        pinMode(col_pins[n], OUTPUT);
        digitalWrite(col_pins[n], 1);
    }
    pinMode(row_pins[0], INPUT_PULLUP);
    pinMode(row_pins[1], INPUT_PULLUP);
    pinMode(row_pins[2], INPUT_PULLUP);
    pinMode(row_pins[3], INPUT);

    fspi.begin(36, 37, 35, TFT_CS);
    tft.begin(78000000);

    tft.fillScreen(ILI9341_BLACK);
    tft.setRotation(3);

    r1.begin(13, 12, CLICKS_PER_STEP);
    r2.begin(16, 17, CLICKS_PER_STEP);
    r3.begin(18, 21, CLICKS_PER_STEP);
    r4.begin(38, 37, CLICKS_PER_STEP);
    timer = timerBegin(0, 80, true);
    timerAttachInterrupt(timer, &handleLoop, true);
    timerAlarmWrite(timer, 100, true);
    timerAlarmEnable(timer);



    WiFi.mode(WIFI_STA);
    esp_wifi_set_mac(WIFI_IF_STA, myAddress);

    if (esp_now_init() == ESP_OK) {
        //Serial.println("ESPNow Init success");
    } else {
        //Serial.println("ESPNow Init fail");
        return;
    }
    esp_now_register_recv_cb(messageReceived);

    memcpy(peerInfo.peer_addr, receiverAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        //Serial.println("Failed to add peer");
        return;
    }


    for (n = 0; n < 6; n++) {
        last_values.pos[n] = rx_data.values.pos[n] + 1;
        last_values.leds = rx_data.values.leds;
    }
    last_values.ow_feed = rx_data.values.ow_feed + 1;
    last_values.ow_rapid = rx_data.values.ow_rapid + 1;
    last_values.ow_spindle = rx_data.values.ow_spindle + 1;
    last_values.jog_scale = rx_data.values.jog_scale + 1;


}


void matrix_read() {
    uint8_t sw = 0;
    uint8_t n = 0;
    digitalWrite(row_pins[3], 0);
    pinMode(row_pins[3], INPUT);
    for (sw = 0; sw < 6; sw++) {
        for (n = 0; n < 6; n++) {
            pinMode(col_pins[n], INPUT);
        }
        pinMode(col_pins[sw], OUTPUT);
        digitalWrite(col_pins[sw], 0);
        sw_stat[0][sw] = digitalRead(row_pins[0]);
        sw_stat[1][sw] = digitalRead(row_pins[1]);
        sw_stat[2][sw] = digitalRead(row_pins[2]);
    }


    for (n = 0; n < 6; n++) {
        pinMode(col_pins[n], INPUT);
    }
    pinMode(row_pins[3], OUTPUT);
    digitalWrite(row_pins[3], 1);

    for (n = 0; n < 6; n++) {
        if ((rx_data.values.leds & (1<<n)) != 0) {
            pinMode(col_pins[n], OUTPUT);
            digitalWrite(col_pins[n], 0);
        } else {
            pinMode(col_pins[n], INPUT);
        }
    }

}


void update_stats() {
    uint8_t n = 0;
    for (n = 0; n < 6; n++) {
        if (rx_data.values.pos[n] > 99999.0) {
            rx_data.values.pos[n] = 99999.0;
        }
        if (rx_data.values.pos[n] > 99999.0) {
            rx_data.values.pos[n] = 99999.0;
        }
    }

    tx_data.values.jog = r1.getPosition();
    r1.resetPosition(0);


    tx_data.values.buttons = 0;
    for (n = 0; n < 6; n++) {
        if (sw_stat[0][n] == 0) {
            tx_data.values.buttons |= (1<<n);
        }
    }
    for (n = 0; n < 6; n++) {
        if (sw_stat[1][n] == 0) {
            tx_data.values.buttons |= (1<<(n+6));
        }
    }
    for (n = 0; n < 6; n++) {
        if (sw_stat[2][n] == 0) {
            tx_data.values.buttons |= (1<<(n+12));
        }
    }
}



void loop() {
    uint8_t sw = 0;
    uint8_t n = 0;
    uint8_t nr = 0;

    float batt_voltage = 0.0;


    for (n = 0; n < 100; n++) {
        batt_voltage += (float)analogRead(ADC);
    }
    batt_voltage = batt_voltage / 100.0 / 1550.0;


    matrix_read();
    tx_data.values.ow_feed = r2.getPosition();
    tx_data.values.ow_rapid = r3.getPosition();
    tx_data.values.ow_spindle = r4.getPosition();

    uint8_t rx_buffer[rx_data_t_size];
    uint8_t tx_buffer[tx_data_t_size];

    Serial.println("############");

    Serial.print(tx_data.values.ow_feed);
    Serial.print(" ");
    Serial.print(tx_data.values.ow_rapid);
    Serial.print(" ");
    Serial.print(tx_data.values.ow_spindle);
    Serial.print(" ");
    Serial.print(tx_data.values.jog);
    Serial.println();

    tft.setTextSize(3);
    tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);

    int ln = 0;
    int row_n = 0;
    int rmap[3] = {0, 2, 1};
    for (row_n = 0; row_n < 3; row_n++) {
        for (ln = 0; ln < 6; ln++) {
            Serial.print(" ");
            Serial.print(sw_stat[rmap[row_n]][ln]);
            tft.setCursor(60 + 30 * ln, 70 + 30 * row_n);
            tft.setTextColor(ILI9341_RED, ILI9341_BLACK);
            if (sw_stat[rmap[row_n]][ln] == 0) {
                tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
                tft.print("X");
            } else {
                tft.setTextColor(ILI9341_RED, ILI9341_BLACK);
                tft.print("0");
            }
        }
        Serial.println();
    }

    tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);

    tft.setCursor(70, 20);
    tft.print(tx_data.values.ow_feed);
    tft.print(" ");

    tft.setCursor(70 + 60 * 1, 20);
    tft.print(tx_data.values.ow_rapid);
    tft.print(" ");

    tft.setCursor(70 + 60 * 2, 20);
    tft.print(tx_data.values.ow_spindle);
    tft.print(" ");

    tft.setCursor(130, 170);
    tft.print(tx_data.values.jog);
    tft.print(" ");

    tft.setCursor(10, 218);
    tft.print(batt_voltage);
    tft.print("V ");

    tft.setCursor(200, 218);
    tft.print(rx_counter);
    tft.print(" ");


    rx_data.values.leds += 1;



    delay(5);

}
