cmake_minimum_required(VERSION 3.12)
project(proj_error LANGUAGES CXX)

add_executable(proj_error src/sample_function.cpp src/main.cpp)
target_include_directories(proj_error
                           PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
