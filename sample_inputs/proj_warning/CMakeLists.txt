cmake_minimum_required(VERSION 3.12)
project(proj_warning LANGUAGES CXX)

add_executable(proj_warning src/sample_function.cpp src/main.cpp)
target_include_directories(proj_warning
                           PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
