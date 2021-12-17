//https://github.com/WorldFamousElectronics/PulseSensorPlayground

#ifndef PULSE_H
#define PULSE_H
#define USE_ARDUINO_INTERRUPTS true // Set-up low-level interrupts for most acurate BPM math.
#include "Arduino.h"
#include <PulseSensorPlayground.h>


class PULSE{
    private:
        PulseSensorPlayground pulseSensor;
    
    public:
        PULSE(byte p, int t, int led);  // constructor
        int getBPM();
        void setThreshold(int t);
        bool sawBeat();

};

#endif


PULSE::PULSE(byte p, int t=500, int led=13){
    pulseSensor.analogInput(p);
    pulseSensor.setThreshold(t);
    pulseSensor.blinkOnPulse(led);    //auto-magically blink Arduino's LED with heartbeat.
    pulseSensor.begin();
}

int PULSE::getBPM(){
  int myBPM = pulseSensor.getBeatsPerMinute();
  if(myBPM > 200) return -1;
  return myBPM;
}

void PULSE::setThreshold(int t){
    pulseSensor.setThreshold(t);
}

bool PULSE::sawBeat(){
    return pulseSensor.sawStartOfBeat();
}