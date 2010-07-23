# CMakeLists.txt: cmake config file for SunPinyin 2 build on Mac

include(CheckIncludeFiles)
include(CheckFunctionExists)

cmake_minimum_required(VERSION 2.6)
project(SUNPINYIN)

set(CMAKE_OSX_ARCHITECTURES x86_64;i386)

set(PACKAGE             sunpinyin)
set(GETTEXT_PACKAGE     ${PACKAGE})
set(PACKAGE_NAME        ${PACKAGE})
set(PACKAGE_BUGREPORT   "sunpinyin-developers@googlegroups.com")
set(PACKAGE_TARNAME     ${PACKAGE})
set(MAJOR_VERSION       2)
set(MINOR_VERSION       0)
set(BUILD_VERSION       2)
set(VERSION             ${MAJOR_VERSION}.${MINOR_VERSION})
set(PACKAGE_SOVERSION   3)
set(PACKAGE_VERSION     ${VERSION})
set(PACKAGE_STRING      "${PACKAGE} ${VERSION}")

option(TRAIN_LM
       "Set to ON to train language model using lexicon and corpus, otherwise I will download it from open-gram."
       OFF)

check_include_files(assert.h    HAVE_ASSERT_H)
check_include_files(dlfcn.h     HAVE_DLFCN_H)
check_include_files(fcntl.h     HAVE_FCNTL_H)
check_include_files(getopt.h    HAVE_GETOPT_H)
check_include_files(iconv.h     HAVE_ICONV_H)
check_include_files(inttypes.h  HAVE_INTTYPES_H)
check_include_files(libintl.h   HAVE_LIBINTL_H)
check_include_files(limit.h     HAVE_LIMIT_H)
check_include_files(locale.h    HAVE_LOCALE_H)
check_include_files(stdlib.h    HAVE_STDLIB_H)
check_include_files(string.h    HAVE_STRING_H)
check_include_files(strings.h   HAVE_STRINGS_H)
check_include_files(memory.h    HAVE_MEMORY_H)
check_include_files(stdint.h    HAVE_STDINT_H)
check_include_files(wchar.h     HAVE_WCHAR_H)
check_include_files(unistd.h    HAVE_UNISTD_H)
check_include_files(sys/mman.h  HAVE_SYS_MMAN_H)
check_include_files(sys/stat.h  HAVE_SYS_STAT_H)
check_include_files(sys/types.h HAVE_SYS_TYPES_H)

check_function_exists(getopt_long HAVE_GETOPT_LONG)
check_function_exists(getpagesize HAVE_GETPAGESIZE)
check_function_exists(gettext     HAVE_GETTEXT)
check_function_exists(get_opt     HAVE_GET_OPT)
check_function_exists(munmap      HAVE_MUNMAP)
check_function_exists(memset      HAVE_MEMSET)
check_function_exists(setlocale   HAVE_SETLOCALE)
check_function_exists(strdup      HAVE_STRDUP)
check_function_exists(strndup     HAVE_STRNDUP)
check_function_exists(strlen      HAVE_STRLEN)
check_function_exists(strcpy      HAVE_STRCPY)
check_function_exists(log2        HAVE_LOG2)
check_function_exists(exp2        HAVE_EXP2)


if (APPLE)
    set(HOST_OS "mac")
    set(SKIP_ICONV_LIBRARY 0)
elseif (${CMAKE_SYSTEM_NAME} MATCHES Linux)
    set(HOST_OS "linux")
    set(SKIP_ICONV_LIBRARY 1)
elseif (${CMAKE_SYSTEM_NAME} MATCHES SunOS)
    set(HOST_OS "solaris")
    set(SKIP_ICONV_LIBRARY 1)
endif (APPLE)

include(TestBigEndian)
test_big_endian(WORDS_BIGENDIAN)

configure_file(src/config/${HOST_OS}.h
               ${CMAKE_SOURCE_DIR}/src/host_os.h ESCAPE_QUOTES)
configure_file(config.h.cmakein config.h ESCAPE_QUOTES)

add_definitions(-DHAVE_CONFIG_H)
if (NOT DEFINED SUNPINYIN_DATA_DIR)
    add_definitions(-DSUNPINYIN_DATA_DIR="${CMAKE_INSTALL_PREFIX}/share/${PACKAGE}/data")
endif (NOT DEFINED SUNPINYIN_DATA_DIR)

set(SOURCE_DIR      "${SUNPINYIN_SOURCE_DIR}/src")
set(SLM_SRC_DIR     "${SOURCE_DIR}/slm")
set(LEXICON_SRC_DIR "${SOURCE_DIR}/lexicon")
set(IMECORE_DIR     "${SOURCE_DIR}/ime-core")
set(PINYIN_SRC_DIR  "${SOURCE_DIR}/pinyin")
set(TSLMENDIAN_DIR  "${SLM_SRC_DIR}/tslmendian")

include_directories(${CMAKE_CURRENT_BINARY_DIR} ${SOURCE_DIR} ${PINYIN_SRC_DIR} ${IMECORE_DIR} ${TSLMENDIAN_DIR})

set(CORPUS_DIR      "${SUNPINYIN_SOURCE_DIR}/raw")
set(RESULT_DIR      "${SUNPINYIN_SOURCE_DIR}/data")
set(SWAP_DIR        "${SUNPINYIN_SOURCE_DIR}/swap")
set(LMTARGET        "lm_sc")

add_subdirectory(src)
add_subdirectory(build EXCLUDE_FROM_ALL)
add_subdirectory(data)

configure_file(sunpinyin.pc.in sunpinyin.pc @ONLY)
install(FILES sunpinyin.pc
    DESTINATION lib/pkgconfig)

set(CPACK_PACKAGE_NAME ${PACKAGE_NAME})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "an SLM based input method engine")
set(CPACK_PACKAGE_VERSION_MAJOR ${MAJOR_VERSION})
set(CPACK_PACKAGE_VERSION_MINOR ${MINOR_VERSION})
set(CPACK_PACKAGE_VERSION_PATCH ${BUILD_VERSION})
set(CPACK_SOURCE_IGNORE_FILES "/.git/;.gitignore;/cmakebuild")
set(CPACK_SOURCE_GENERATOR "TBZ2")
include(CPack)

message(STATUS)
message(STATUS "===== ${PACKAGE_STRING} ====")
message(STATUS "MAKE_INSTALL_PREFIX = ${CMAKE_INSTALL_PREFIX}")
message(STATUS "TRAIN_LM = ${TRAIN_LM}")
message(STATUS "HOST_OS = ${HOST_OS}")
message(STATUS "WORDS_BIGENDIAN = ${WORDS_BIGENDIAN}")
message(STATUS "SUNPINYIN_DATA_DIR = ${SUNPINYIN_DATA_DIR}")
message(STATUS "Change a value with: cmake -D<variable>=<value>")
message(STATUS "==========")
message(STATUS)

# cache the options
set(TRAIN_LM ${TRAIN_LM} CACHE BOOL "Generate data/lm_sc.t3g from corpus and lexicon")

