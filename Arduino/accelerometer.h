#ifndef ACCELEROMETER_H
#define ACCELEROMETER_H
#include "Arduino.h"
#include <MPU6050.h>
#include <I2Cdev.h>
#include <math.h>
#include <Wire.h>

class ACCELEROMETER{
    private:
        MPU6050* mpu_1;
        int16_t ax1, ay1, az1, gx1, gy1, gz1;   //mpu1
        double theta_x1, theta_y1, theta_z1;    //mpu1的變化角度
        bool moving_x1, moving_y1, moving_z1;   //mpu1的xyz方向現在是否在移動
        MPU6050* mpu_2;
        int16_t ax2, ay2, az2, gx2, gy2, gz2;   //mpu2
        double theta_x2, theta_y2, theta_z2;    //mpu2的變化角度
        bool moving_x2, moving_y2, moving_z2;   //mpu2的xyz方向現在是否在移動

    public:
        ACCELEROMETER();
        bool available(int index);
        void update();
        bool is_moving(int t1, int t2);
        bool is_moving_mpu1(int t);
        bool is_moving_mpu2(int t);
        ~ACCELEROMETER();
};

#endif

ACCELEROMETER::ACCELEROMETER(){
    Wire.begin();
    mpu_1 = new MPU6050(0x68);
    mpu_2 = new MPU6050(0x69);
    mpu_1->initialize();
    mpu_2->initialize();
}

bool ACCELEROMETER::available(int index=0){
    switch (index) {
        case 1:
            return mpu_1->testConnection();
        case 2:
            return mpu_2->testConnection();
        default:
            return (mpu_1->testConnection() && mpu_2->testConnection());
    }
}

void ACCELEROMETER::update(){
    //mpu1
    mpu_1->getMotion6(&ax1, &ay1, &az1, &gx1, &gy1, &gz1);
    theta_x1 = atan(ax1 / sqrt(square(ay1) + square(az1))) * 180 / 3.14;
    theta_y1 = atan(ay1 / sqrt(square(ax1) + square(az1))) * 180 / 3.14;
    theta_z1 = atan(sqrt(square(ax1) + square(ay1)) / az1) * 180 / 3.14;

    //mpu2
    mpu_2->getMotion6(&ax2, &ay2, &az2, &gx2, &gy2, &gz2);
    theta_x2 = atan(ax2 / sqrt(square(ay2) + square(az2))) * 180 / 3.14;
    theta_y2 = atan(ay2 / sqrt(square(ax2) + square(az2))) * 180 / 3.14;
    theta_z2 = atan(sqrt(square(ax2) + square(ay2)) / az2) * 180 / 3.14;
}

bool ACCELEROMETER::is_moving(int t1=30, int t2=30){
    return (is_moving_mpu1(t1) && is_moving_mpu2(t2));
}

bool ACCELEROMETER::is_moving_mpu1(int t=30){
    moving_x1 = fabs(theta_x1 + 90) > t;
    moving_y1 = fabs(theta_y1) > t;
    moving_z1 = fabs(theta_z1 - 90) > t;
    return (moving_x1 && moving_y1 && moving_z1);
}

bool ACCELEROMETER::is_moving_mpu2(int t=30){
    moving_x2 = fabs(theta_x2 + 90) > t;
    moving_y2 = fabs(theta_y2) > t;
    moving_z2 = fabs(theta_z2 - 90) > t;
    return (moving_x2 && moving_y2 && moving_z2);
}

ACCELEROMETER::~ACCELEROMETER(){
    delete mpu_1;
    delete mpu_2;
}
