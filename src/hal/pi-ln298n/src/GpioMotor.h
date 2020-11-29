//
// Created by phil on 21.03.20.
//

#ifndef GPIOCPP_GPIOWHEEL_H
#define GPIOCPP_GPIOWHEEL_H
namespace pi_ln298n{

using GpioId = unsigned int;
class GpioMotor
{
public:
    GpioMotor(GpioId forward, GpioId backward, GpioId enable);
    void set(float effort);
    void stop();
    ~GpioMotor();
protected:
    void initialize();
    void forward(float effortPerc);
    void backward(float effortPerc);
    int effort2pwm(float effortPerc);
    static unsigned int _nInstances;
    GpioId _forward,_backward,_enable;
};

}
#endif //GPIOCPP_GPIOWHEEL_H
