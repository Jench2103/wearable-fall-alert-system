#define USE_ARDUINO_INTERRUPTS true // Set-up low-level interrupts for most acurate BPM math.
#include "sensor.h"
#include "bluetooth.h"
/////mpu6050/////
#include <MPU6050.h>
#include <I2Cdev.h>
#include <math.h>
#include <Wire.h>
MPU6050 mpu_1(0x68);
int16_t prev_accx1 = 0;
int16_t prev_accy1 = 0;
int16_t prev_accz1 = 0;
MPU6050 mpu_2(0x69);
int16_t prev_accx2 = 0;
int16_t prev_accy2 = 0;
int16_t prev_accz2 = 0;
bool mpu_available(int index=0);
bool is_moving(int t1=30, int t2=30);

GPS gps;
PULSE pulse(3);
BUZZER buzzer(7);
BLUETOOTH bluetooth;
int button = 5;
bool send = false;
bool debug = true;

void setup()
{
    Serial.begin(9600);
    Wire.begin();
    mpu_1.initialize();
    mpu_2.initialize();
    pinMode(button, OUTPUT); 
}

void loop()
{
    //數值更新
    if(gps.enable())    //更新gps位置
        gps.locationUpdate();

    //事件發生
    if(is_moving && !send){
        double location[2] = {gps.getLongitude(), gps.getLatitude()};
        int BPM = pulse.getBPM();
        bluetooth.arduino_to_phone(location[0], location[1], BPM);
        send = true;
    }

    if(bluetooth.if_buzzer_on == 1){   //兩分鐘內，app傳送打開蜂鳴器的訊息
        buzzer.on();
    }else if(bluetooth.if_buzzer_on == 0){    //兩分鐘內，app傳送"不用"打開蜂鳴器的訊息
        send = false;
        bluetooth.reset();
    }
    
    if(digitalRead(button)){   //兩分鐘後，arduino上的蜂鳴器
        buzzer.off();
        send = false;
        bluetooth.reset();
    }
}


bool mpu_available(int index=0){
    switch (index) {
        case 1:
            return mpu_1.testConnection();
        case 2:
            return mpu_2.testConnection();
        default:
            return (mpu_1.testConnection() && mpu_2.testConnection());
    }
}

bool is_moving(int t1=3, int t2=3){   //mpu1及mpu2的xyz方向現在是否在移動
    int16_t ax1, ay1, az1, gx1, gy1, gz1;   //mpu1
    float accx1 = ((float)(ax1 - prev_accx2) / 16384) * ((float)(ax1 - prev_accx2) / 16384);
    float accy1 = ((float)(ay1 - prev_accy2) / 16384) * ((float)(ay1 - prev_accy2) / 16384);
    float accz1 = ((float)(az1 - prev_accz2) / 16384) * ((float)(az1 - prev_accz2) / 16384);

    prev_accx2 = ax1;
    prev_accy2 = ay1;
    prev_accz2 = az1;

    int16_t ax2, ay2, az2, gx2, gy2, gz2;   //mpu2
    float accx2 = ((float)(ax2 - prev_accx2) / 16384) * ((float)(ax2 - prev_accx2) / 16384);
    float accy2 = ((float)(ay2 - prev_accy2) / 16384) * ((float)(ay2 - prev_accy2) / 16384);
    float accz2 = ((float)(az2 - prev_accz2) / 16384) * ((float)(az2 - prev_accz2) / 16384);
    
    prev_accx2 = ax2;
    prev_accy2 = ay2;
    prev_accz2 = az2;

    if(debug){
        Serial.print("Acc1: ");
        Serial.println(sqrt(accx1 + accy1 + accz1));
        Serial.print("Acc2: ");
        Serial.println(sqrt(accx2 + accy2 + accz2));
    }

    return sqrt(accx1 + accy1 + accz1) > t1 && sqrt(accx2 + accy2 + accz2) > t2;
}
