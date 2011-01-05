set(DICTFILE		 "${CORPUS_DIR}/dict.utf8")
set(CORPUSFILE		 "${CORPUS_DIR}/corpus.utf8")

set(IDS_FILE		 "${SWAP_DIR}/${LMTARGET}.ids")
set(SWAP_FILE		 "${SWAP_DIR}/swap")
set(IDNGRAM_FILE3	 "${SWAP_DIR}/${LMTARGET}.id3gram")
set(RAW_LM_FILE3	 "${SWAP_DIR}/${LMTARGET}.3gram")
set(SLM_FILE3		 "${SWAP_DIR}/${LMTARGET}.3gm")
set(PYTRIE_PRINTOUT      "${SWAP_DIR}/pydict_sc.log.utf8")
set(TSLM_INFO_FILE3      "${SWAP_DIR}/${LMTARGET}.t3g.arpa")

set(TSLM_FILE3		 "${RESULT_DIR}/${LMTARGET}.t3g")
set(PYTRIE_FILE          "${RESULT_DIR}/pydict_sc.bin")

if (SKIP_ICONV_LIBRARY)
    set(ICONV_LIBRARY "")
else (SKIP_ICONV_LIBRARY)
    find_library(ICONV_LIBRARY iconv)
    if (NOT ICONV_LIBRARY)
        message(FATAL_ERROR "Couldn't find iconv library")
    endif (NOT ICONV_LIBRARY)
endif (SKIP_ICONV_LIBRARY)

set(MMSEG_SOURCES
    ${SOURCE_DIR}/config.h
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h 
    ${SLM_SRC_DIR}/sim_dict.cpp ${SLM_SRC_DIR}/sim_dict.h
    ${SLM_SRC_DIR}/sim_sen.cpp ${SLM_SRC_DIR}/sim_sen.h
    ${SLM_SRC_DIR}/mmseg/mmseg.cpp)

add_executable(mmseg EXCLUDE_FROM_ALL ${MMSEG_SOURCES})
target_link_libraries(mmseg ${ICONV_LIBRARY})

set(IDS2NGRAM_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/sim_fmerge.h
    ${SLM_SRC_DIR}/ids2ngram/ids2ngram.cpp ${SLM_SRC_DIR}/ids2ngram/idngram.h
    ${SLM_SRC_DIR}/ids2ngram/idngram_merge.h)

add_executable(ids2ngram EXCLUDE_FROM_ALL ${IDS2NGRAM_SOURCES})
target_link_libraries(ids2ngram ${ICONV_LIBRARY})

set(SLMTHREAD_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/sim_slm.cpp ${SLM_SRC_DIR}/sim_slm.h
    ${SLM_SRC_DIR}/thread/ValueCompress.cpp ${SLM_SRC_DIR}/thread/ValueCompress.h
    ${SLM_SRC_DIR}/thread/slmthread.cpp)

add_executable(slmthread EXCLUDE_FROM_ALL ${SLMTHREAD_SOURCES})
target_link_libraries(slmthread ${ICONV_LIBRARY})

set(SLMBUILD_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/sim_slm.h
    ${SLM_SRC_DIR}/sim_slmbuilder.cpp ${SLM_SRC_DIR}/sim_slmbuilder.h
    ${SLM_SRC_DIR}/slmbuild/slmbuild.cpp)

add_executable(slmbuild EXCLUDE_FROM_ALL ${SLMBUILD_SOURCES})
target_link_libraries(slmbuild ${ICONV_LIBRARY})

set(SLMPRUNE_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/sim_slm.cpp ${SLM_SRC_DIR}/sim_slm.h
    ${SLM_SRC_DIR}/slmprune/slmprune.cpp)

add_executable(slmprune EXCLUDE_FROM_ALL ${SLMPRUNE_SOURCES})
target_link_libraries(slmprune ${ICONV_LIBRARY})

set(TSLMINFO_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/slm.cpp ${SLM_SRC_DIR}/slm.h
    ${SLM_SRC_DIR}/sim_slm.h
    ${SLM_SRC_DIR}/tslminfo/tslminfo.cpp)

add_executable(tslminfo EXCLUDE_FROM_ALL ${TSLMINFO_SOURCES})
target_link_libraries(tslminfo ${ICONV_LIBRARY})

add_custom_command(
    OUTPUT ${IDS_FILE}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/mmseg -d ${DICTFILE} -f bin -s 10 -a 9 ${CORPUSFILE} >${IDS_FILE}
    DEPENDS mmseg ${DICTFILE})

add_custom_command(
    OUTPUT ${IDNGRAM_FILE3}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/ids2ngram -n 3 -s ${SWAP_FILE} -o ${IDNGRAM_FILE3} -p 5000000 ${IDS_FILE}
    COMMAND rm -f ${SWAP_FILE}
    DEPENDS ids2ngram ${IDS_FILE})

add_custom_command(
    OUTPUT ${RAW_LM_FILE3}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/slmbuild -n 3 -o ${RAW_LM_FILE3} -w 120000 -c 0,2,2 -d ABS,0.0005 -d ABS -d ABS,0.6 -b 10 -e 9 ${IDNGRAM_FILE3}
    DEPENDS slmbuild ${IDNGRAM_FILE3})

if (TRAIN_LM)
    add_custom_command(
        OUTPUT ${SLM_FILE3}
        COMMAND ${CMAKE_CURRENT_BINARY_DIR}/slmprune ${RAW_LM_FILE3} ${SLM_FILE3} R 100000 1250000 1000000
        DEPENDS slmprune ${RAW_LM_FILE3})
endif (TRAIN_LM)

add_custom_command(
    OUTPUT ${TSLM_FILE3}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/slmthread ${SLM_FILE3} ${TSLM_FILE3}
    DEPENDS slmthread ${SLM_FILE3})

add_custom_command(
    OUTPUT ${TSLM_INFO_FILE3}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tslminfo -p -v -l ${DICTFILE} ${TSLM_FILE3} >${TSLM_INFO_FILE3}
    DEPENDS tslminfo ${DICTFILE} ${TSLM_FILE3})

add_custom_target(
    trigram
    DEPENDS ${TSLM_INFO_FILE3})

set(GENPYT_SOURCES 
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/slm.cpp ${SLM_SRC_DIR}/slm.h
    ${TSLMENDIAN_DIR}/writer.cpp ${TSLMENDIAN_DIR}/writer.h
    ${LEXICON_SRC_DIR}/trie_writer.cpp ${LEXICON_SRC_DIR}/trie_writer.h
    ${LEXICON_SRC_DIR}/genPYT.cpp ${LEXICON_SRC_DIR}/pytrie.cpp ${LEXICON_SRC_DIR}/pytrie.h
    ${LEXICON_SRC_DIR}/pytrie_gen.cpp ${LEXICON_SRC_DIR}/pytrie_gen.h
    ${PINYIN_SRC_DIR}/pinyin_data.cpp ${PINYIN_SRC_DIR}/pinyin_data.h
    ${PINYIN_SRC_DIR}/syllable.h)

set(TSLMPACK_SOURCES
    ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/slm.cpp ${SLM_SRC_DIR}/slm.h
    ${SLM_SRC_DIR}/thread/ValueCompress.cpp ${SLM_SRC_DIR}/thread/ValueCompress.h
    ${SLM_SRC_DIR}/tslmpack/slmpack.cpp ${SLM_SRC_DIR}/tslmpack/common.h
    ${SLM_SRC_DIR}/tslmpack/arpa_conv.cpp ${SLM_SRC_DIR}/tslmpack/arpa_conv.h
    ${SLM_SRC_DIR}/tslmpack/arpa_slm.cpp ${SLM_SRC_DIR}/tslmpack/arpa_slm.h)

add_executable(tslmpack EXCLUDE_FROM_ALL ${TSLMPACK_SOURCES})

set(GENPYT_SOURCES
    ${SOURCE_DIR}/portability.cpp ${SOURCE_DIR}/portability.h ${SOURCE_DIR}/config.h
    ${SLM_SRC_DIR}/slm.cpp ${SLM_SRC_DIR}/slm.h
    ${TSLMENDIAN_DIR}/writer.cpp ${TSLMENDIAN_DIR}/writer.h
    ${LEXICON_SRC_DIR}/trie_writer.cpp ${LEXICON_SRC_DIR}/trie_writer.h
    ${LEXICON_SRC_DIR}/genPYT.cpp ${LEXICON_SRC_DIR}/pytrie.cpp ${LEXICON_SRC_DIR}/pytrie.h
    ${LEXICON_SRC_DIR}/pytrie_gen.cpp ${LEXICON_SRC_DIR}/pytrie_gen.h
    ${PINYIN_SRC_DIR}/pinyin_data.cpp ${PINYIN_SRC_DIR}/pinyin_data.h
    ${PINYIN_SRC_DIR}/syllable.h)

add_executable(genpyt EXCLUDE_FROM_ALL ${GENPYT_SOURCES})
target_link_libraries(genpyt ${ICONV_LIBRARY})

add_custom_command(
    OUTPUT ${PYTRIE_FILE}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/genpyt -i ${DICTFILE} -o ${PYTRIE_FILE} -l ${PYTRIE_PRINTOUT} -s ${TSLM_FILE3}
    DEPENDS genpyt ${DICTFILE} ${TSLM_FILE3})

add_custom_target(
    tslmfile
    DEPENDS ${TSLM_FILE3})

add_custom_target(
    lexicon
    DEPENDS ${PYTRIE_FILE})

add_custom_target(
    train
    DEPENDS lexicon tslmfile)
