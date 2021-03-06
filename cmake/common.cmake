if(${CMAKE_BUILD_TYPE} MATCHES Debug)
    message("Debug mode")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -march=native -O0 -g -Wall -Wextra")
else()
    message("Release mode")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -march=native -O3 -Wall -Wextra")
endif()

if(DEBUG_TRANSFORMATIONS)
    add_definitions("-DDEBUG_TRANSFORMATIONS")
endif()
