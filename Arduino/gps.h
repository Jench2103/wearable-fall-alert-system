//https://randomnerdtutorials.com/guide-to-neo-6m-gps-module-with-arduino/
//http://arduiniana.org/libraries/tinygpsplus/

#ifndef GPS_H
#define GPS_H
#include "Arduino.h"
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

class GPS{
    private:
        SoftwareSerial GPSSerial; // RX, TX
        TinyGPSPlus gps;

    public:
        GPS();
        bool enable();
        bool locationUpdated();
        double getLatitude();
        double getLongitude();
        double getAltitude();
        String getDateAndTime();
        
};

#endif

GPS::GPS():GPSSerial(3, 4){
    GPSSerial.begin(9600);
}

bool GPS::enable(){
    return GPSSerial.available();
}

bool GPS::locationUpdated(){
    if(GPSSerial.available()){
        gps.encode(GPSSerial.read());
        return true;
    }
    return false;
}

double GPS::getLatitude(){
    return gps.location.lat();
}

double GPS::getLongitude(){
    return gps.location.lng();
}

double GPS::getAltitude(){
    return gps.altitude.meters();
}

String GPS::getDateAndTime(){
    /*
    String date = String(gps.date.year()) + '-' + String(gps.date.month()) + '-' +String(gps.date.day());
    String time = String(gps.time.hour()) + ':' + String(gps.time.minute()) + ':' + String(gps.time.second());
    return date + ' ' + time;
    */

    int date[3] = {gps.date.year(), gps.date.month(), gps.date.day()};
    int time[3] = {gps.time.hour(), gps.time.minute(), gps.time.second()};
    time[0] += 8; //手動加時區
    if(time[0] >= 24){
        time[0] -= 24;
        date[2] += 1;

        if(date[2] == 31 && (date[1] == 1 || date[1] == 3 || date[1] == 5 || date[1] == 7 || date[1] == 8 || date[1] == 10 || date[1] == 12)){
            if(date[1] == 12){
                date[0] += 1;
                date[1] = 1;
            }else{
                date[1] += 1;
            }
            date[2] = 1;
        }else if(date[2] == 30 && (date[1] == 4 || date[1] == 6 || date[1] == 9 || date[1] == 11)){
            date[1] += 1;
            date[2] = 1;
        }else if((date[2] == 28 || date[2] == 29) && date[1] == 2){ //處理閏年
            if (date[2] == 28 && ((date[0] % 4 == 0 && date[0] % 100 != 0) || date[0] % 400 == 0)){
                date[2] = 29;
            }else{
                date[1] = 3;
                date[2] = 1;
            }
        }else{
            date[2] += 1;
        }
    }

    String str_date = String(date[0]) + '-' + (String(date[1]).length() == 2? String(date[1]) : '0' + String(date[1]))
        + '-' + (String(date[2]).length() == 2? String(date[2]) : '0' + String(date[2]));
    String str_time = (String(time[0]).length() == 2? String(time[0]) : '0' + String(time[0])) 
        + ':' + (String(time[1]).length() == 2? String(time[1]) : '0' + String(time[1]))
        + ':' + (String(time[2]).length() == 2? String(time[2]) : '0' + String(time[2]));
    return str_date + ' ' + str_time;
}