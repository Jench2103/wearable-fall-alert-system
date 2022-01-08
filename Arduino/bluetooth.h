#ifndef BLUETOOTH_H
#define BLUETOOTH_H
#include "Arduino.h"
#include <SoftwareSerial.h>

class BLUETOOTH
{
public:
    BLUETOOTH();
    int n_after_point_lo = 5;                                                   // gps_longtitude傳送時小數點後的位數
    int n_after_point_la = 5;                                                   // gps_latitude傳送時小數點後的位數

    // 接收手機藍芽傳的訊號，回傳值: if_buzzer_on 
    // 收到'0': 不開啟蜂鳴器
    // 收到'a': 傳使用者資訊給手機，開啟蜂鳴器
    int phone_to_arduino(bool event, double gps_longtitude = 0, double gps_latitude = 0, int bpm = 0); 
    int if_buzzer_on = -1;  // 未收到指示: -1；不要開啟蜂鳴器: 0；開啟蜂鳴器: 1
    
    void send_1_to_phone(); // 藍芽傳'1'給手機

    void reset(); // 事件結束，將if_buzzer_on回復預設值-1

private:
    SoftwareSerial BTSerial;
    
    void arduino_to_phone(double gps_longtitude, double gps_latitude, int bpm); // 事件發生時傳送地點、心律等資訊至手機，傳送格式: ，傳送格式: "&heart_rate=76&gps_longitude=121.7654&gps_latitude=23.84723"
};

#endif

BLUETOOTH::BLUETOOTH() : BTSerial(10, 11) // setup // 宣告10腳位為Arduino的RX 、11為Arduino的 TX
{
    BTSerial.begin(9600);
}

int BLUETOOTH::phone_to_arduino(bool event, double gps_longtitude = 0, double gps_latitude = 0, int bpm = 0) // 接收手機藍芽傳的訊號: 傳使用者資訊/是否開啟蜂鳴器
{
    if (BTSerial.available())
    {
        
        char message_from_phone = BTSerial.read();

        switch(message_from_phone)
        {            
            //收到'0': 不開啟蜂鳴器
            case '0':
                if_buzzer_on = 0;
                break;
            //收到'a': 傳使用者資訊給手機，開啟蜂鳴器
            case 'a':
                if_buzzer_on = 1;
                arduino_to_phone(gps_longtitude, gps_latitude, bpm);
                break;
            default:
                break;
        }
    }

    return if_buzzer_on;
}

void BLUETOOTH::reset() // 事件結束，將if_buzzer_on回復預設值-1
{
    if_buzzer_on = -1;
}

void BLUETOOTH::send_1_to_phone() // 藍芽傳'1'給手機
{
    BTSerial.print('1');
}

void BLUETOOTH::arduino_to_phone(double gps_longtitude, double gps_latitude, int bpm) // 事件發生時傳送地點、心律等資訊至手機，傳送格式: &heart_rate=76&gps_longitude=121.7654&gps_latitude=23.84723
{
    String string_to_phone;
    string_to_phone = "&heart_rate=" + (String(bpm).length() == 3? String(bpm) : '0' + String(bpm)) + "&gps_longitude=" + String(gps_longtitude, n_after_point_lo) + "&gps_latitude=" + String(gps_latitude, n_after_point_la);

    BTSerial.print(string_to_phone);
}
