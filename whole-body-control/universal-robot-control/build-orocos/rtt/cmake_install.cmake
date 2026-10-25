# Install script for directory: /workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt" TYPE FILE FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Activity.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/ArgumentDescription.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Attribute.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/BufferPolicy.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Component.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/ConfigurationInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/ConnPolicy.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/DataFlowInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/ExecutionEngine.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/FactoryExceptions.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/FlowStatus.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Handle.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/InputPort.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Logger.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Logger.inl"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Operation.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/OperationCaller.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/OperationInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/OperationInterfacePart.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/OutputPort.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Port.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Property.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/PropertyBag.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/RTT.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/SendHandle.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/SendStatus.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Service.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/ServiceRequester.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/TaskContext.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/Time.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/rt_string.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/rtt-detail-fwd.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/rtt-fwd.hpp"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt" TYPE FILE FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/rtt-config.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/os/tlsf" TYPE FILE FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/os/tlsf/tlsf.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/orocos-rtt-gnulinux.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8.99"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/liborocos-rtt-gnulinux.so.2.8.99"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/liborocos-rtt-gnulinux.so.2.8"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8.99"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/liborocos-rtt-gnulinux.so")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/os/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/base/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/internal/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/types/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/typekit/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/transports/corba/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/transports/mqueue/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/scripting/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/marsh/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/plugin/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/deployment/cmake_install.cmake")
  include("/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/extras/cmake_install.cmake")

endif()

