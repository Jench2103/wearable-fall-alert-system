#include "sensor.h"

/////gps/////
GPS::GPS() : GPSSerial(3, 4)
{
    GPSSerial.begin(9600);
}

bool GPS::enable()
{
    return GPSSerial.available();
}

bool GPS::locationUpdate()
{
    if (GPSSerial.available())
    {
        gps.encode(GPSSerial.read());
        return true;
    }
    return false;
}

double GPS::getLongitude()
{
    return gps.location.lng();
}

double GPS::getLatitude()
{
    return gps.location.lat();
}

double GPS::getAltitude()
{
    return gps.altitude.meters();
}

String GPS::getLocation()
{
    return '(' + String(gps.location.lat()) + ',' + String(gps.location.lng()) + ')';
}

String GPS::getDateAndTime()
{
    /*
    String date = String(gps.date.year()) + '-' + String(gps.date.month()) + '-' +String(gps.date.day());
    String time = String(gps.time.hour()) + ':' + String(gps.time.minute()) + ':' + String(gps.time.second());
    return date + ' ' + time;
    */

    int date[3] = {gps.date.year(), gps.date.month(), gps.date.day()};
    int time[3] = {gps.time.hour(), gps.time.minute(), gps.time.second()};
    time[0] += 8; //手動加時區
    if (time[0] >= 24)
    {
        time[0] -= 24;
        date[2] += 1;

        if (date[2] == 31 && (date[1] == 1 || date[1] == 3 || date[1] == 5 || date[1] == 7 || date[1] == 8 || date[1] == 10 || date[1] == 12))
        {
            if (date[1] == 12)
            {
                date[0] += 1;
                date[1] = 1;
            }
            else
            {
                date[1] += 1;
            }
            date[2] = 1;
        }
        else if (date[2] == 30 && (date[1] == 4 || date[1] == 6 || date[1] == 9 || date[1] == 11))
        {
            date[1] += 1;
            date[2] = 1;
        }
        else if ((date[2] == 28 || date[2] == 29) && date[1] == 2)
        { //處理閏年
            if (date[2] == 28 && ((date[0] % 4 == 0 && date[0] % 100 != 0) || date[0] % 400 == 0))
            {
                date[2] = 29;
            }
            else
            {
                date[1] = 3;
                date[2] = 1;
            }
        }
        else
        {
            date[2] += 1;
        }
    }

    String str_date = String(date[0]) + '-' + (String(date[1]).length() == 2 ? String(date[1]) : '0' + String(date[1])) + '-' + (String(date[2]).length() == 2 ? String(date[2]) : '0' + String(date[2]));
    String str_time = (String(time[0]).length() == 2 ? String(time[0]) : '0' + String(time[0])) + ':' + (String(time[1]).length() == 2 ? String(time[1]) : '0' + String(time[1])) + ':' + (String(time[2]).length() == 2 ? String(time[2]) : '0' + String(time[2]));
    return str_date + ' ' + str_time;
}

/////pulse/////
PULSE::PULSE(byte p, int t = 500, int led = 13)
{
    pulseSensor.analogInput(p);
    pulseSensor.setThreshold(t);
    pulseSensor.blinkOnPulse(led); //auto-magically blink Arduino's LED with heartbeat.
    pulseSensor.begin();
}

int PULSE::getBPM()
{
    int myBPM = pulseSensor.getBeatsPerMinute();
    if (myBPM > 200)
        return 200;
    if (myBPM < 60)
        return 60;
    return myBPM;
}

void PULSE::setThreshold(int t)
{
    pulseSensor.setThreshold(t);
}

bool PULSE::sawBeat()
{
    return pulseSensor.sawStartOfBeat();
}

/////buzzer/////
BUZZER::BUZZER(byte p, bool state = LOW) : pin(p)
{
    pinMode(pin, OUTPUT);
    digitalWrite(pin, state);
}

byte BUZZER::getPin()
{
    return pin;
}

void BUZZER::on()
{
    digitalWrite(pin, HIGH);
}

void BUZZER::off()
{
    digitalWrite(pin, LOW);
}

bool BUZZER::getState()
{
    return digitalRead(pin);
}
