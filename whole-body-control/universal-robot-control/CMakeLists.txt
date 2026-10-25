
cmake_minimum_required(VERSION 3.25)

project(universal_robot_control VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Dependencies
find_package(pinocchio REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(GTest REQUIRED)

# Core robotics library
add_library(urc_core
    src/robot_model.cpp
    src/computed_torque.cpp
    src/cartesian_impedance.cpp
)

target_include_directories(urc_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(urc_core PUBLIC
    pinocchio::pinocchio
    Eigen3::Eigen
)

target_compile_options(urc_core PRIVATE
    -Wall
    -Wextra
    -Wpedantic
)

# Existing robot demo
add_executable(urc_demo
    src/main.cpp
)

target_link_libraries(urc_demo PRIVATE
    urc_core
)

# Existing dynamics tests
enable_testing()

add_executable(urc_tests
    tests/test_dynamics.cpp
)

target_link_libraries(urc_tests PRIVATE
    urc_core
    GTest::gtest_main
)

include(GoogleTest)

gtest_discover_tests(
    urc_tests
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
