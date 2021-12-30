#include "bluetooth_test_1230.h"

// 測試: RXD接10，TXD接11，GND接GND，VDC接3.3V

//在序列埠監控視窗輸入't': 將事件設定為true
//在序列埠監控視窗輸入'f': 將事件設定為false
//在序列埠監控視窗輸入's': 藍芽傳'1'給手機


//手機傳送'a'給: 
//  事件為true: 
//    事件剛變為true: 藍芽傳'1'給手機
//    其他: 藍芽傳"23.55555,120.55555,millis()%1000;"給手機
//  事件為false: 
//    藍芽傳'0'給手機

//手機傳送'0'給藍芽: 在序列埠監控視窗顯示"收到'0'，不開蜂鳴器"，重置事件

//手機傳送'1'給藍芽: 在序列埠監控視窗顯示"收到'1'，開蜂鳴器"，重置事件

//
double t1 = 23.555555555555555;
double t2 = 120.55555555555555;
int t3;
bool event_test = false;
//

BLUETOOTH BT;


void setup()
{
    Serial.begin(9600);
    Serial.print("generate BT\n");
}

void loop()
{

    t3 = millis()%1000;
    
    if(Serial.available())
    {
      char a = Serial.read();

      if (event_test && a == 'f') // 由t變f
        {
            Serial.println("");
            Serial.println("**event_test = t -> f");
            BT.reset();
            event_test = false;
        }
        else if (a == 'f')
        {
            Serial.println("");
            Serial.println("**event_test = f");
            event_test = false;
        }
        else if (a == 't')
        {
            Serial.println("");
            Serial.println("**event_test = t");
            event_test = true;
        }
        if (a == 's')
            BT.send1();
    }
    
    BT.phone_to_arduino(event_test, t1, t2, t3);
     
    if(BT.if_buzzer_on == 0 || BT.if_buzzer_on == 1)
    {
      BT.reset();
      event_test = false;
    }
}
