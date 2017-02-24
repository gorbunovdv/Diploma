cmake_minimum_required(VERSION 3.3)
project(Diploma)

include(cmake/common.cmake)

set(SOURCE_FILES main.cpp managers/filter_transformation_manager.h data_structures/transformations_iterator.h)

find_package(Armadillo REQUIRED)
include_directories(${ARMADILLO_INCLUDE_DIRS})
add_executable(Diploma ${SOURCE_FILES})

target_link_libraries(Diploma ${ARMADILLO_LIBRARIES} jsoncpp)
