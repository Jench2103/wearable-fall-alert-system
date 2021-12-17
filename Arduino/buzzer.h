#ifndef BUZZER_H
#define BUZZER_H
#include "Arduino.h"

class BUZZER{
    private:
        byte pin;
    
    public:
        BUZZER(byte p, bool state = LOW);    // constructor
        byte getPin();
        void on();
        void off();
        bool getState();
};

#endif


BUZZER::BUZZER(byte p, bool state = LOW):pin(p){
    pinMode(pin,OUTPUT);
    digitalWrite(pin,state);
}

byte BUZZER::getPin(){
    return pin;
}

void BUZZER::on(){
    digitalWrite(pin,HIGH);
}

void BUZZER::off(){
    digitalWrite(pin,LOW);
}

bool BUZZER::getState(){
    return digitalRead(pin);
}

