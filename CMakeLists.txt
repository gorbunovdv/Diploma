cmake_minimum_required(VERSION 3.3)
project(Diploma)

include(cmake/common.cmake)

set(SOURCE_FILES main.cpp /usr/local/include/json/json.h)

add_executable(Diploma ${SOURCE_FILES})

target_link_libraries(Diploma jemalloc)
