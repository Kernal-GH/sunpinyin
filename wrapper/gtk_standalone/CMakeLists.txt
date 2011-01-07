# CMakeLists.txt: cmake config file for ibus-sunpinyin

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0005 NEW)
endif(COMMAND cmake_policy)

cmake_minimum_required(VERSION 2.6)
project(SUNPINYIN)

find_package(PkgConfig REQUIRED)

pkg_check_modules(SunPinyin sunpinyin-2.0 REQUIRED)

add_definitions(-DICON_PATH="${CMAKE_SOURCE_DIR}/icons")
add_subdirectory (src)

