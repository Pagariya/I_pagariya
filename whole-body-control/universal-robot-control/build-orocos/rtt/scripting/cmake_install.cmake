# Install script for directory: /workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/scripting" TYPE FILE FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ArgumentsParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CallFunction.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandBinary.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandComposite.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandCounter.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandDataSource.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandFunctors.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandIllegal.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandNOP.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommandString.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/CommonParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionBool.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionBoolDataSource.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionBoolProperty.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionCache.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionCompare.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionComposite.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionDSDuration.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionDuration.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionExpire.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionFalse.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionInvert.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionOnce.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ConditionTrue.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/DataSourceCondition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/DataSourceTime.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/DumpObject.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/EdgeCondition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ExpressionParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/FunctionFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/FunctionGraph.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/FunctionGraphBuilder.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/GraphCopier.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ParsedStateMachine.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/Parser.Main.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/Parser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/PeerParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ProgramExceptions.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ProgramGraphParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ProgramInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ProgramService.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/PropertyParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ScriptParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/Scripting.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ScriptingService.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/SendHandleAlias.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateDescription.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateGraphParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateInterface.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateMachine.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateMachineBuilder.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StateMachineService.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/StatementProcessor.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/TryCommand.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ValueChangeParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/ValueParser.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/VertexNode.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/parse_exception.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/parser-debug.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/parser-types.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/scripting/rtt-scripting-fwd.hpp"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins/librtt-scripting-gnulinux.so.2.8.99"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins/librtt-scripting-gnulinux.so.2.8"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "/workspaces/I_pagariya/whole-body-control/universal-robot-control/.local/orocos/lib/orocos/gnulinux/types:/workspaces/I_pagariya/whole-body-control/universal-robot-control/.local/orocos/lib")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins" TYPE SHARED_LIBRARY FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/scripting/librtt-scripting-gnulinux.so.2.8.99"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/scripting/librtt-scripting-gnulinux.so.2.8"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins/librtt-scripting-gnulinux.so.2.8.99"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins/librtt-scripting-gnulinux.so.2.8"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHANGE
           FILE "${file}"
           OLD_RPATH "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
           NEW_RPATH "/workspaces/I_pagariya/whole-body-control/universal-robot-control/.local/orocos/lib/orocos/gnulinux/types:/workspaces/I_pagariya/whole-body-control/universal-robot-control/.local/orocos/lib")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/orocos/gnulinux/plugins" TYPE SHARED_LIBRARY FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/scripting/librtt-scripting-gnulinux.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/scripting" TYPE FILE FILES "/workspaces/I_pagariya/whole-body-control/universal-robot-control/build-orocos/rtt/scripting/rtt-scripting-config.h")
endif()

