# Install script for directory: /workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/os" TYPE FILE FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Atomic.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/CAS.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Condition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/MainThread.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Mutex.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/MutexLock.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/OS.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Semaphore.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/StartStopManager.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Thread.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/ThreadInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Time.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/TimeService.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/Timer.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/fosi.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/fosi_interface.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/fosi_internal_interface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/main.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/oro_allocator.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/oro_arch.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/oro_arch_interface.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/oro_limits.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/oro_malloc.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rint.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rt_list.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rtconversions.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rtstreambufs.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rtstreams.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/rtt-os-fwd.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/startstop.h"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/threads.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/traces.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/gnulinux/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/lxrt/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/xenomai/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/ecos/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/macosx/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/win32/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_i386/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_x86_64/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_powerpc/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_msvc/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_noasm/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/oro_gcc/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/targets/cmake_install.cmake")

endif()

