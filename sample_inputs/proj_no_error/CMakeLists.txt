cmake_minimum_required(VERSION 3.12)
project(proj_no_error LANGUAGES CXX)

add_executable(proj_no_error src/sample_function.cpp src/main.cpp)
target_include_directories(proj_no_error
                           PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
