cmake_minimum_required(VERSION 3.1.0)
project(videostream)

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
include_directories(include)
include_directories(${OpenCV_INCLUDE_DIRS})

link_directories(${PROJECT_SOURCE_DIR})

# python 
include_directories("/usr/local/include/python3.6m")
add_library(pyvideostream SHARED "src/pyvideostream.cpp")
target_link_libraries(pyvideostream ${OpenCV_LIBS} hcnetsdk PlayCtrl)
set_target_properties(pyvideostream PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/../" PREFIX "")
