# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build

# Include any dependencies generated for this target.
include CMakeFiles/PyEsegment.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/PyEsegment.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/PyEsegment.dir/flags.make

CMakeFiles/PyEsegment.dir/py.cpp.o: CMakeFiles/PyEsegment.dir/flags.make
CMakeFiles/PyEsegment.dir/py.cpp.o: ../py.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/PyEsegment.dir/py.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/PyEsegment.dir/py.cpp.o -c /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/py.cpp

CMakeFiles/PyEsegment.dir/py.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/PyEsegment.dir/py.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/py.cpp > CMakeFiles/PyEsegment.dir/py.cpp.i

CMakeFiles/PyEsegment.dir/py.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/PyEsegment.dir/py.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/py.cpp -o CMakeFiles/PyEsegment.dir/py.cpp.s

CMakeFiles/PyEsegment.dir/py.cpp.o.requires:

.PHONY : CMakeFiles/PyEsegment.dir/py.cpp.o.requires

CMakeFiles/PyEsegment.dir/py.cpp.o.provides: CMakeFiles/PyEsegment.dir/py.cpp.o.requires
	$(MAKE) -f CMakeFiles/PyEsegment.dir/build.make CMakeFiles/PyEsegment.dir/py.cpp.o.provides.build
.PHONY : CMakeFiles/PyEsegment.dir/py.cpp.o.provides

CMakeFiles/PyEsegment.dir/py.cpp.o.provides.build: CMakeFiles/PyEsegment.dir/py.cpp.o


# Object files for target PyEsegment
PyEsegment_OBJECTS = \
"CMakeFiles/PyEsegment.dir/py.cpp.o"

# External object files for target PyEsegment
PyEsegment_EXTERNAL_OBJECTS =

/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: CMakeFiles/PyEsegment.dir/py.cpp.o
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: CMakeFiles/PyEsegment.dir/build.make
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudabgsegm.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudaobjdetect.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudastereo.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_dnn.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_ml.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_shape.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_stitching.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_superres.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_videostab.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudafeatures2d.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudacodec.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudaoptflow.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudalegacy.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_calib3d.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudawarping.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_features2d.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_flann.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_highgui.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_objdetect.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_photo.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudaimgproc.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudafilters.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudaarithm.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_video.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_videoio.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_imgcodecs.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_imgproc.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_core.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: /usr/local/lib/libopencv_cudev.so.3.4.0
/home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so: CMakeFiles/PyEsegment.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library /home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/PyEsegment.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/PyEsegment.dir/build: /home/sfe/workspace/dest_linux/SFE/thirdparty/PyEsegment.so

.PHONY : CMakeFiles/PyEsegment.dir/build

CMakeFiles/PyEsegment.dir/requires: CMakeFiles/PyEsegment.dir/py.cpp.o.requires

.PHONY : CMakeFiles/PyEsegment.dir/requires

CMakeFiles/PyEsegment.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/PyEsegment.dir/cmake_clean.cmake
.PHONY : CMakeFiles/PyEsegment.dir/clean

CMakeFiles/PyEsegment.dir/depend:
	cd /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build /home/sfe/workspace/dest_linux/SFE/thirdparty/Esegment/build/CMakeFiles/PyEsegment.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/PyEsegment.dir/depend

