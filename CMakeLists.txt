cmake_minimum_required(VERSION 2.8)
project(Diploma)

include(cmake/common.cmake)

set(SOURCE_FILES main.cpp managers/filter_transformation_manager.h data_structures/transformations_iterator.h utils.h managers/classes_distribution_manager.h)

add_executable(Diploma ${SOURCE_FILES})

target_link_libraries(Diploma jsoncpp jemalloc)
