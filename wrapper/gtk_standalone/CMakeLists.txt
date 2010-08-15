# CMakeLists.txt: cmake config file for ibus-sunpinyin

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0005 NEW)
endif(COMMAND cmake_policy)

cmake_minimum_required(VERSION 2.6)
project(SUNPINYIN)

find_package(PkgConfig)
if (NOT PKG_CONFIG_FOUND)
    message(FATAL_ERROR "Couldn't find pkg-config to proceed.")
endif (NOT PKG_CONFIG_FOUND)

pkg_check_modules(SunPinyin_PKGCONF sunpinyin-2.0)
find_path(SunPinyin_INCLUDE_DIR
    NAMES sunpinyin.h
    PATHS ${SunPinyin_PKGCONF_INCLUDE_DIRS}
)

find_library(SunPinyin_LIBRARY
  NAMES sunpinyin
  PATHS ${SunPinyin_PKGCONF_LIBRARY_DIRS}
)

add_definitions(-DICON_PATH="${CMAKE_SOURCE_DIR}/icons")
add_subdirectory (src)

