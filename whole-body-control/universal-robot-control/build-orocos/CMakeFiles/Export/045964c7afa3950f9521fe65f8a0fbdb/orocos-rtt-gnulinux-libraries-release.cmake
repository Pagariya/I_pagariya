#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "imported_rtt-typekit-gnulinux_plugin" for configuration "Release"
set_property(TARGET imported_rtt-typekit-gnulinux_plugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(imported_rtt-typekit-gnulinux_plugin PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "imported_orocos-rtt-gnulinux_dynamic"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/orocos/gnulinux/types/librtt-typekit-gnulinux.so.2.8.99"
  IMPORTED_SONAME_RELEASE "librtt-typekit-gnulinux.so.2.8"
  )

list(APPEND _cmake_import_check_targets imported_rtt-typekit-gnulinux_plugin )
list(APPEND _cmake_import_check_files_for_imported_rtt-typekit-gnulinux_plugin "${_IMPORT_PREFIX}/lib/orocos/gnulinux/types/librtt-typekit-gnulinux.so.2.8.99" )

# Import target "imported_orocos-rtt-gnulinux_dynamic" for configuration "Release"
set_property(TARGET imported_orocos-rtt-gnulinux_dynamic APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(imported_orocos-rtt-gnulinux_dynamic PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "/usr/lib/x86_64-linux-gnu/libboost_filesystem.so;/usr/lib/x86_64-linux-gnu/libboost_system.so;/usr/lib/x86_64-linux-gnu/libboost_serialization.so;/usr/lib/x86_64-linux-gnu/libpthread.a;rt;dl"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8.99"
  IMPORTED_SONAME_RELEASE "liborocos-rtt-gnulinux.so.2.8"
  )

list(APPEND _cmake_import_check_targets imported_orocos-rtt-gnulinux_dynamic )
list(APPEND _cmake_import_check_files_for_imported_orocos-rtt-gnulinux_dynamic "${_IMPORT_PREFIX}/lib/liborocos-rtt-gnulinux.so.2.8.99" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
