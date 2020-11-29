cmake_minimum_required(VERSION 3.10)
project(pi_ln298n)

set(CMAKE_CXX_STANDARD 14)
set(COMPILE_FOR_PI TRUE CACHE BOOL "Set true if compile for pi")
set(COMPILE_TESTS FALSE CACHE BOOL "Set true if compile for pi")

if(NOT COMPILE_FOR_PI)
    set(target_sources src/pigpiostub.h src/pigpiostub.cpp)
endif()

add_library(${PROJECT_NAME} ${target_sources} src/GpioMotor.h src/GpioMotor.cpp)

if(COMPILE_FOR_PI)
    target_compile_definitions(${PROJECT_NAME} PRIVATE COMPILE_FOR_PI)
endif()

target_include_directories(${PROJECT_NAME} PUBLIC src)
target_include_directories(${PROJECT_NAME} PUBLIC include)

if(COMPILE_FOR_PI)
    target_link_libraries(${PROJECT_NAME} -lpigpio)
endif()

if(COMPILE_TESTS)
    add_executable(test_gpiomotor test/test.cpp)
    target_link_libraries(test_gpiomotor ${PROJECT_NAME})
endif()


