# CMakeLists.txt: cmake config file for ibus-sunpinyin

find_package(GTK2 REQUIRED gtk)

include_directories(${GTK2_INCLUDE_DIRS} ${SunPinyin_INCLUDE_DIRS})
set(LIBS ${LIBS} ${GTK2_LIBRARIES} ${SunPinyin_LIBRARIES})
set(STANDALONE_SRCS imi_gtkwin.cpp sunpinyin.cpp)

add_executable(sunpinyin ${STANDALONE_SRCS})
target_link_libraries(sunpinyin ${LIBS})

