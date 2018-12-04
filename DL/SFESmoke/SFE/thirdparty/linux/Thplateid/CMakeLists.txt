cmake_minimum_required(VERSION 3.1.0)
project(pythplateid)

# c++11 required
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
endif ()

if (CMAKE_SYSTEM_NAME MATCHES "Darwin")
    set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "/usr/local/opt/opencv-3.2.0")
endif ()

# OpenVC3 required
find_package(OpenCV 3.2 REQUIRED)

# where to find header files
include_directories(.)
include_directories(include)
include_directories(${OpenCV_INCLUDE_DIRS})

# python
include_directories("/usr/local/include/python3.6m")
include_directories(thplateid)
add_library(pythplateid SHARED "pythplateid.cpp")
target_link_libraries(pythplateid ${OpenCV_LIBS} ${PROJECT_SOURCE_DIR}/thplateid/libthplateid.so)
set_target_properties(pythplateid PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/../" PREFIX "")

SET_TARGET_PROPERTIES(PROPERTIES RUNTIME_OUTPUT_DIRECTORY  "${CMAKE_BINARY_DIR}/../")