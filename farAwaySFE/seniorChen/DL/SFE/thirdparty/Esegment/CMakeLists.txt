cmake_minimum_required(VERSION 3.1.0)
project(Esegment)

# c++11 required
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
endif ()

# OpenVC3 required
find_package(OpenCV 3.2 REQUIRED)

# where to find header files
include_directories(${PROJECT_SOURCE_DIR})
include_directories(${OpenCV_INCLUDE_DIRS})

# lib
# add_library(Esegment STATIC segment-image.h segment-graph.h disjoint-set.h)
# set_target_properties(Esegment PROPERTIES LINKER_LANGUAGE CXX)

# python 
include_directories("/usr/local/include/python3.6m")
add_library(PyEsegment SHARED py.cpp)
target_link_libraries(PyEsegment ${OpenCV_LIBS})
set_target_properties(PyEsegment PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/../" PREFIX "")
