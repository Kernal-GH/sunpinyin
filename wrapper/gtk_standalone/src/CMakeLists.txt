# CMakeLists.txt: cmake config file for ibus-sunpinyin

find_package(GTK2 REQUIRED gtk)
find_library(ICONV_LIBRARY iconv)

find_library(SunPinyin_LIBRARY
  NAMES sunpinyin
  PATHS ${SunPinyin_LIBRARY_DIRS}
)

include_directories(${GTK2_INCLUDE_DIRS} ${SunPinyin_INCLUDE_DIRS})
set(LIBS ${LIBS} ${GTK2_LIBRARIES} ${SunPinyin_LIBRARIES} ${ICONV_LIBRARY})
set(STANDALONE_SRCS imi_gtkwin.cpp sunpinyin.cpp)

add_executable(gtk_standalone ${STANDALONE_SRCS})
message(STATUS "${LIBS}")
target_link_libraries(gtk_standalone ${LIBS})
