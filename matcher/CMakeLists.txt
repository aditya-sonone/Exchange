add_library(matcher

    matcher.cpp
    orderqueue.cpp
    orderbook.cpp
)

target_include_directories(matcher PUBLIC
    ${CMAKE_SOURCE_DIR}/generated
)