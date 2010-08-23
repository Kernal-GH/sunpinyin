if (CMAKE_BUILD_TYPE STREQUAL "Debug" OR
    CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo" )
    add_definitions("-DDEBUG")
endif()

if (NOT SKIP_ICONV_LIBRARY)
    find_library(ICONV_LIBRARY iconv)
endif (NOT SKIP_ICONV_LIBRARY)

set(IME_SOURCES 
    portability.cpp portability.h
    slm/slm.cpp slm/slm.h 
    lexicon/pytrie.cpp lexicon/pytrie.h 
    pinyin/pinyin_data.cpp pinyin/pinyin_data.h 
    pinyin/pinyin_seg.cpp pinyin/pinyin_seg.h 
    pinyin/shuangpin_data.cpp pinyin/shuangpin_data.h 
    pinyin/shuangpin_seg.cpp pinyin/shuangpin_seg.h 
    ime-core/imi_context.cpp ime-core/imi_context.h 
    ime-core/imi_data.cpp ime-core/imi_data.h 
    ime-core/lattice_states.cpp ime-core/lattice_states.h 
    ime-core/imi_view.cpp ime-core/imi_view.h 
    ime-core/imi_uiobjects.cpp ime-core/imi_uiobjects.h 
    ime-core/imi_keys.h 
    ime-core/imi_view_classic.cpp ime-core/imi_view_classic.h 
    ime-core/imi_winHandler.cpp ime-core/imi_winHandler.h 
    ime-core/ic_history.cpp ime-core/ic_history.h 
    ime-core/imi_funcobjs.cpp ime-core/imi_funcobjs.h 
    ime-core/imi_options.cpp ime-core/imi_options.h 
    ime-core/imi_option_event.cpp ime-core/imi_option_event.h 
    ime-core/userdict.cpp ime-core/userdict.h)

if (NOT DEFINED SUNPINYIN_DATA_DIR)
    add_definitions(-DSUNPINYIN_DATA_DIR="${CMAKE_INSTALL_PREFIX}/share/${PACKAGE}/data")
endif (NOT DEFINED SUNPINYIN_DATA_DIR)

add_library(${PACKAGE} SHARED ${IME_SOURCES})
target_link_libraries(${PACKAGE} ${SQLITE3_LIBRARY} ${ICONV_LIBRARY})

set_target_properties(${PACKAGE}
    PROPERTIES
    VERSION ${PACKAGE_VERSION}
    SOVERSION ${PACKAGE_SOVERSION})

add_library(${PACKAGE}-static STATIC ${IME_SOURCES})
SET_TARGET_PROPERTIES(${PACKAGE}-static PROPERTIES OUTPUT_NAME ${PACKAGE})

SET_TARGET_PROPERTIES(${PACKAGE} PROPERTIES CLEAN_DIRECT_OUTPUT 1)
SET_TARGET_PROPERTIES(${PACKAGE}-static PROPERTIES CLEAN_DIRECT_OUTPUT 1)

install(TARGETS ${PACKAGE} ${PACKAGE}-static
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib)

set(GENERAL_HEADERS
    sunpinyin.h
    host_os.h
    portability.h)

set(SLM_HEADERS
    slm/slm.h)

set(LEXICON_HEADERS
    lexicon/pytrie.h)

set(IME_CORE_HEADERS
    ime-core/imi_view_classic.h
    ime-core/imi_uiobjects.h
    ime-core/lattice_states.h
    ime-core/ic_history.h
    ime-core/imi_funcobjs.h
    ime-core/imi_context.h
    ime-core/imi_winHandler.h
    ime-core/userdict.h
    ime-core/imi_option_event.h
    ime-core/imi_data.h
    ime-core/utils.h
    ime-core/imi_keys.h
    ime-core/imi_option_keys.h
    ime-core/imi_options.h
    ime-core/imi_defines.h
    ime-core/imi_view.h)

set(PINYIN_HEADERS
    pinyin/segmentor.h
    pinyin/shuangpin_seg.h
    pinyin/datrie.h
    pinyin/quanpin_trie.h
    pinyin/pinyin_seg.h
    pinyin/pinyin_data.h
    pinyin/syllable.h
    pinyin/shuangpin_data.h
    pinyin/datrie_impl.h)

set(INC_DIR include/${PACKAGE}-${VERSION})
install(FILES ${GENERAL_HEADERS}    DESTINATION ${INC_DIR})
install(FILES ${SLM_HEADERS}        DESTINATION ${INC_DIR}/slm)
install(FILES ${LEXICON_HEADERS}    DESTINATION ${INC_DIR}/lexicon)
install(FILES ${IME_CORE_HEADERS}   DESTINATION ${INC_DIR}/ime-core)
install(FILES ${PINYIN_HEADERS}     DESTINATION ${INC_DIR}/pinyin)

