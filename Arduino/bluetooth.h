#ifndef BLUETOOTH_H
#define BLUETOOTH_H
#include "Arduino.h"
#include <SoftwareSerial.h>

class BLUETOOTH
{
public:
    BLUETOOTH();
    void arduino_to_phone(double gps_longtitude, double gps_latitude, int bpm); // 事件發生時傳送地點、心律等資訊至手機，傳送格式: gps_longtitude,gps_latitude,bpm;
    int n_after_point_lo = 5;                                                   // gps_longtitude傳送時小數點後的位數
    int n_after_point_la = 5;                                                   // gps_latitude傳送時小數點後的位數

    int phone_to_arduino(); // 接收手機藍芽傳的訊號: 是否開啟蜂鳴器，回傳值: if_buzzer_on
    int if_buzzer_on = -1;  // 未收到指示: -1；不要開啟蜂鳴器: 0；開啟蜂鳴器: 1

    void reset();

private:
    SoftwareSerial BTSerial;
};

#endif

BLUETOOTH::BLUETOOTH() : BTSerial(10, 11) // setup // 宣告10腳位為Arduino的RX 、11為Arduino的 TX
{
    BTSerial.begin(38400);
}

void BLUETOOTH::arduino_to_phone(double gps_longtitude, double gps_latitude, int bpm) // 事件發生時傳送地點、心律等資訊至手機，傳送格式: 經度,緯度,心律;
{
    String string_to_phone = String(gps_longtitude, n_after_point_lo) + ',' + String(gps_latitude, n_after_point_la) + ',' + String(bpm) + ';';

    BTSerial.println(string_to_phone);
}

int BLUETOOTH::phone_to_arduino() // 接收手機藍芽傳的訊號: 是否開啟蜂鳴器
{
    if (BTSerial.available())
    {
        char message_from_phone = BTSerial.read();

        if (message_from_phone == '0')
        {
            if_buzzer_on = 0;
        }

        if (message_from_phone == '1')
        {
            if_buzzer_on = 1;
        }
    }

    return if_buzzer_on;
}

void BLUETOOTH::reset() // 事件發生時傳送地點、心律等資訊至手機，傳送格式: 經度,緯度,心律;
{
    if_buzzer_on = -1;
}
