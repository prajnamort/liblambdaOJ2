cmake_minimum_required(VERSION 2.8.7)

project(lambdaOJ2)

set(LIBRARY_OUTPUT_PATH "${PROJECT_BINARY_DIR}/lib")

include_directories ("${PROJECT_SOURCE_DIR}/include")

################### compiler and compile flags ##########################
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -O3")
###################### install include files ############################
install(DIRECTORY include DESTINATION "${CMAKE_INSTALL_PREFIX}")
########################### subdirectory ################################
add_subdirectory(src)
