cmake_minimum_required(VERSION 3.10)

project(Exchange)

set(CMAKE_CXX_STANDARD 17)

find_package(Python3 REQUIRED)

add_custom_command(

    OUTPUT
        ${CMAKE_SOURCE_DIR}/generated/.stamp

    COMMAND
        ${Python3_EXECUTABLE} main.py

    COMMAND
        ${CMAKE_COMMAND} -E touch
        ${CMAKE_SOURCE_DIR}/generated/.stamp

    DEPENDS
        ${CMAKE_SOURCE_DIR}/schemas/order.txt
        ${CMAKE_SOURCE_DIR}/generator/main.py
        ${CMAKE_SOURCE_DIR}/generator/parser.py
        ${CMAKE_SOURCE_DIR}/generator/cpp_generator.py
        ${CMAKE_SOURCE_DIR}/generator/file_writer.py
        ${CMAKE_SOURCE_DIR}/generator/models.py

    WORKING_DIRECTORY
        ${CMAKE_SOURCE_DIR}/generator

    COMMENT
        "Generating protocol code"
)

add_custom_target(protocol_codegen
    DEPENDS
        ${CMAKE_SOURCE_DIR}/generated/.stamp
)

add_subdirectory(matcher)
add_subdirectory(gateway)


add_dependencies(matcher protocol_codegen)
add_dependencies(gateway protocol_codegen)

add_executable(test
    test.cpp
)

target_include_directories(test PRIVATE
    generated
    gateway
)

target_link_libraries(test
    matcher
)

add_dependencies(test protocol_codegen)