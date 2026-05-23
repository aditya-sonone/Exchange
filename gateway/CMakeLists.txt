cmake_minimum_required(VERSION 3.10)

project(Gateway)

set(CMAKE_CXX_STANDARD 17)

add_executable(gateway
    main.cpp
    server.cpp
    handlers/orderhandler.cpp
)

target_include_directories(gateway PRIVATE
    ../generated
    ../matcher
)

target_link_libraries(gateway
    matcher
)