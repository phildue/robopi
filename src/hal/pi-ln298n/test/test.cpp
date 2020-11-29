#include <iostream>

#include <stdio.h>
#include "pi_ln298n/pi_ln298n.h"
#include <thread>

constexpr int enA = 21;
constexpr int enB = 13;
constexpr int in1 = 20;
constexpr int in2 = 16;
constexpr int in3 = 26;
constexpr int in4 = 19;

#include <chrono>
using namespace pi_ln298n;
int main(int argc, char *argv[])
{
    GpioMotor left(in1,in2,enA);
    GpioMotor right(in4,in3,enB);

    auto start = std::chrono::system_clock::now();

    for(int i = 0; i < 60; i++)
    {
        left.set((float)i/60.0f);
        right.set(-1.0f * (float)i/60.0f);
	std::this_thread::sleep_for (std::chrono::milliseconds(500));
    }
    for(int i = 60; i > 0; i--)
    {
        left.set((float)i/60.0f);
        right.set((float)-i/60.0f);
	std::this_thread::sleep_for (std::chrono::milliseconds(500));
    }
    left.stop();
    right.stop();


    return 0;
}
