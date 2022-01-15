#ifndef SENSOR_H
#define SENSOR_H
#include "Arduino.h"

//gps
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

//pulse
//https://github.com/WorldFamousElectronics/PulseSensorPlayground
#include <PulseSensorPlayground.h>

class GPS
{
private:
    SoftwareSerial GPSSerial; // RX, TX
    TinyGPSPlus gps;

public:
    GPS();
    bool enable();
    bool locationUpdate();
    double getLongitude();
    double getLatitude();
    double getAltitude();
    String getLocation();
    String getDateAndTime();
};

class PULSE
{
private:
    PulseSensorPlayground pulseSensor;

public:
    PULSE(byte p, int t = 500, int led = 13); // constructor
    int getBPM();
    void setThreshold(int t);
    bool sawBeat();
};

class BUZZER
{
private:
    byte pin;

public:
    BUZZER(byte p, bool state = LOW); // constructor
    byte getPin();
    void on();
    void off();
    bool getState();
};

#endif
