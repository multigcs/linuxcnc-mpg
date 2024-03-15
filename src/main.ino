
#include <Wire.h> 
#include <ESPRotary.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

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






uint8_t update = 0;
uint8_t axis_selected = 0;


void IRAM_ATTR handleLoop() {
  r1.loop();
  r2.loop();
  r3.loop();
  r4.loop();
}



void setup() {
    uint8_t n = 0;
    Serial.begin(115200);
    Serial.setTimeout(10);
    pinMode(15, OUTPUT);

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
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);


    tft.drawRect(1, 1, 202, 6 * PSTEP + 5 + 2, ILI9341_WHITE);
    tft.drawRect(2, 2, 200, 6 * PSTEP + 5, ILI9341_LIGHTGREY);


    tft.setTextSize(3);
    tft.setTextColor(ILI9341_RED, ILI9341_BLACK);
    tft.setCursor(10, 10 + 0 * PSTEP);
    tft.print("X: ");
    tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
    tft.setCursor(10, 10 + 1 * PSTEP);
    tft.print("Y: ");
    tft.setTextColor(ILI9341_BLUE, ILI9341_BLACK);
    tft.setCursor(10, 10 + 2 * PSTEP);
    tft.print("Z: ");
    tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK);
    tft.setCursor(10, 10 + 3 * PSTEP);
    tft.print("A: ");
    tft.setCursor(10, 10 + 4 * PSTEP);
    tft.print("B: ");
    tft.setCursor(10, 10 + 5 * PSTEP);
    tft.print("C: ");
    tft.setCursor(10, 10 + 6 * PSTEP);

    for (n = 0; n < 6; n++) {
        tx_data.values.jog[n] = 0;
    }

    r1.begin(13, 12, CLICKS_PER_STEP);
    r2.begin(16, 17, CLICKS_PER_STEP);
    r3.begin(18, 21, CLICKS_PER_STEP);
    r4.begin(38, 37, CLICKS_PER_STEP);
    timer = timerBegin(0, 80, true);
    timerAttachInterrupt(timer, &handleLoop, true);
    timerAlarmWrite(timer, 100, true);
    timerAlarmEnable(timer);
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
        //digitalWrite(col_pins[n], 1);
    }
    pinMode(col_pins[axis_selected], OUTPUT);
    digitalWrite(col_pins[axis_selected], 0);
    pinMode(row_pins[3], OUTPUT);
    digitalWrite(row_pins[3], 1);
}






void loop() {
    uint8_t sw = 0;
    uint8_t n = 0;
    uint8_t nr = 0;

    matrix_read();
    tx_data.values.ow_feed = r2.getPosition();
    tx_data.values.ow_rapid = r3.getPosition();
    tx_data.values.ow_spindle = r4.getPosition();

    if (sw_stat[1][0] == 0) {
        axis_selected = 0;
    } else if (sw_stat[1][1] == 0) {
        axis_selected = 1;
    } else if (sw_stat[1][2] == 0) {
        axis_selected = 2;
    } else if (sw_stat[1][3] == 0) {
        axis_selected = 3;
    } else if (sw_stat[1][4] == 0) {
        axis_selected = 4;
    } else if (sw_stat[1][5] == 0) {
        axis_selected = 5;
    }


    uint8_t rx_buffer[rx_data_t_size];
    uint8_t tx_buffer[tx_data_t_size];
    uint8_t rlen = Serial.readBytes(rx_buffer, rx_data_t_size);

    if (rlen == rx_data_t_size) {
        for (n = 0; n < rx_data_t_size; n++) {
            rx_data.data[n] = rx_buffer[n];
        }

        for (n = 0; n < 6; n++) {
            if (rx_data.values.pos[n] > 99999.0) {
                rx_data.values.pos[n] = 99999.0;
            }
            if (rx_data.values.pos[n] > 99999.0) {
                rx_data.values.pos[n] = 99999.0;
            }
        }

        if (axis_selected >= 0 && axis_selected < 6) {
           tx_data.values.jog[axis_selected] += r1.getPosition();
        }
        r1.resetPosition(0);


        tx_data.values.buttons = 0;
        for (n = 0; n < 6; n++) {
            if (sw_stat[0][n] == 0) {
                tx_data.values.buttons |= (1<<n);
            }
        }
        for (n = 0; n < 6; n++) {
            if (sw_stat[2][n] == 0) {
                tx_data.values.buttons |= (1<<(n+6));
            }
        }


        for (n = 0; n < tx_data_t_size; n++) {
            tx_buffer[n] = tx_data.data[n];
        }
        Serial.write(tx_buffer, tx_data_t_size);

    }

    tft.setTextSize(3);
    tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);

    if (update >= 0 && update < 6) {
        tft.setCursor(50, 10 + update * PSTEP);
        sprintf(tmp_str, "%08.2f", rx_data.values.pos[update]);
        tft.print(tmp_str);

    } else if (update == 6) {

        nr = 0;
        tft.setTextSize(1);
        tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);
        tft.setCursor(215, 5 + nr * 47 + 5);
        tft.print("Feed:");
        tft.setTextSize(3);
        tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
        tft.setCursor(230, 5 + nr * 45 + 20);
        sprintf(tmp_str, "%3i%%", rx_data.values.ow_feed);
        tft.print(tmp_str);

    } else if (update == 7) {
        nr = 1;
        tft.setTextSize(1);
        tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);
        tft.setCursor(215, 5 + nr * 47 + 5);
        tft.print("Rapid:");
        tft.setTextSize(3);
        tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
        tft.setCursor(230, 5 + nr * 45 + 20);
        sprintf(tmp_str, "%3i%%", rx_data.values.ow_rapid);
        tft.print(tmp_str);
    } else if (update == 8) {
        nr = 2;
        tft.setTextSize(1);
        tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);
        tft.setCursor(215, 5 + nr * 47 + 5);
        tft.print("Spindle:");
        tft.setTextSize(3);
        tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
        tft.setCursor(230, 5 + nr * 45 + 20);
        sprintf(tmp_str, "%3i%%", rx_data.values.ow_spindle);
        tft.print(tmp_str);
    } else if (update == 9) {
        nr = 3;
        tft.setTextSize(1);
        tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);
        tft.setCursor(215, 5 + nr * 47 + 5);
        tft.print("Jog:");
        tft.setTextSize(3);
        tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
        tft.setCursor(230, 5 + nr * 45 + 20);
        sprintf(tmp_str, "%3i%%", 0);
        tft.print(tmp_str);
    } else if (update == 10) {
        nr = 4;
        tft.setTextSize(1);
        tft.setTextColor(ILI9341_LIGHTGREY, ILI9341_BLACK);
        tft.setCursor(215, 5 + nr * 47 + 5);
        tft.print("Misc:");
        tft.setTextSize(3);
        tft.setTextColor(ILI9341_GREEN, ILI9341_BLACK);
        tft.setCursor(230, 5 + nr * 45 + 20);
        sprintf(tmp_str, "%3i%%", 0);
        tft.print(tmp_str);
    }


    if (update < 10) {
        update++;
    } else {
        update = 0;
    }


    delay(15);

}
