cmake_minimum_required(VERSION 3.10)

project(Exchange)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(gateway)

add_executable(test
    test.cpp
    gateway/handlers/orderhandler.cpp
)

target_include_directories(test PRIVATE
    generated
    gateway
)