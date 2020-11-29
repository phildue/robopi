//
// Created by phil on 29.03.20.
//

#ifndef PIGPIOSTUB_H
#define PIGPIOSTUB_H

#define PI_OUTPUT 1
#define PI_INITIALISED 0
#include <vector>
#include <iostream>

static float pwmDutyCycle = 0;
static std::vector<float> pins = std::vector<float>(50);

int gpioInitialise(){
    return PI_INITIALISED;
}
void gpioSetMode(int pin,int sig)
{

}


void gpioWrite(int pin,int sig)
{
    if(sig != pins[pin])
    {
        std::cout << "Setting " << pin << ": " << sig << std::endl;
    }
    pins[pin] = sig;
}
void gpioPWM(int pin,float sig)
{
    if(sig != pins[pin])
    {
        std::cout << "Setting " << pin << ": " << sig << std::endl;
    }
    pins[pin] = sig;
}
int gpioRead(int pin)
{
    return 0;
}

void gpioTerminate()
{

}

float gpioGetPWMdutycycle(int pin)
{
    return pins[pin];
}

void gpioSetPWMfrequency(int pin,int freq)
{
}
#endif //PIGPIOSTUB_H
