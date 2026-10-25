# Install script for directory: /workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspaces/I_pagariya/whole-body-control/universal-robot-control/.local/orocos")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/extras" TYPE FILE FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/Activities.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/Execution.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/FileDescriptorActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/FileDescriptorActivityInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/FileDescriptorSimulationActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/IRQActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/MultiVector.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/MultiVectorComposition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/Orocos.Main.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/PeriodicActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/Properties.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/ReadOnlyPointer.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/SequentialActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/SimulationActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/SimulationThread.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/SlaveActivity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/TaskContexts.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/TimerThread.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/extras/rtt-extras-fwd.hpp"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/extras/dev/cmake_install.cmake")

endif()

