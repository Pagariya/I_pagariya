# Install script for directory: /workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/rtt/types" TYPE FILE FILES
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/BoostArrayTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/CArrayTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/CompositionFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/EnumTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/GlobalsRepository.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/MemberFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/OperatorTypes.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/Operators.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/PrimitiveSequenceTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/PrimitiveTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/PropertyComposition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/PropertyDecomposition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/SequenceConstructor.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/SequenceTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/SequenceTypeInfoBase.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/StdVectorTemplateTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/StreamFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/StructTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TemplateCompositionFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TemplateConnFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TemplateConstructor.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TemplateTypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TemplateValueFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TransportPlugin.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeConstructor.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeInfo.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeInfoGenerator.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeInfoName.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeInfoRepository.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeMarshaller.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeStream-io.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeStream.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeStreamSelector.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypeTransporter.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypekitPlugin.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/TypekitRepository.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/Types.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/ValueFactory.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/VectorTemplateComposition.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/carray.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/rtt-types-fwd.hpp"
    "/workspaces/I_pagariya/whole-body-control/universal-robot-control/third_party/orocos-rtt/rtt/types/type_discovery.hpp"
    )
endif()

