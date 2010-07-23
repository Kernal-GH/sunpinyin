
set(DICTFILE             "${CORPUS_DIR}/dict.utf8")
set(CORPUSFILE           "${CORPUS_DIR}/corpus.utf8")
set(LM_SC_ARPA           "${RESULT_DIR}/lm_sc.t3g.arpa")
set(TSLM_FILE3           "${RESULT_DIR}/${LMTARGET}.t3g")

find_program(WGET_EXECUTABLE wget)
find_program(CURL_EXECUTABLE curl)

if (WGET_EXECUTABLE)
    set(WGET_CMD ${WGET_EXECUTABLE})
    set(WGET_FOUND TRUE)
elseif (CURL_EXECUTABLE)
    set(WGET_CMD "${CURL_EXECUTABLE} -O")
    set(WGET_FOUND TRUE)
else(WGET_EXECUTABLE)
    set(WGET_FOUND FALSE)
    message(SEND_ERROR "Couldn't download lexicon and language model. You can put them where I can reach.")
endif(WGET_EXECUTABLE)

if (CMAKE_SYSTEM_NAME MATCHES SunOS)
    set(TAR_CMD gtar)
else (CMAKE_SYSTEM_NAME MATCHES SunOS)
    set(TAR_CMD tar)
endif (CMAKE_SYSTEM_NAME MATCHES SunOS)

function(add_download_from_og target lm_file)
    if (NOT WGET_FOUND)
        message(FATAL_ERROR "Couldn't find wget/curl. Please install either of them or download ${url} manually.")
    endif (NOT WGET_FOUND)
    set(LM_URL_ROOT "http://open-gram.googlecode.com/files")
    add_custom_target (${target}
        COMMAND ${WGET_CMD} ${LM_URL_ROOT}/${lm_file}
        COMMAND ${TAR_CMD} -xjf ${lm_file} -C ${CMAKE_CURRENT_SOURCE_DIR}
        COMMAND rm -f ${lm_file}
        WORKING_DIRECTORY ${SWAP_DIR}
        COMMENT "Downloading ${lm_file} ..."
    )
endfunction(add_download_from_og)

add_download_from_og(get_lm_sc lm_sc.t3g.arpa.tar.bz2)
add_download_from_og(get_dict dict.utf8.tar.bz2)

add_custom_target(og_data
    DEPENDS  og_lm_sc og_dict)

if (NOT TRAIN_LM)
    add_custom_command(
        OUTPUT ${TSLM_FILE3}
        COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tslmpack ${LM_SC_ARPA} ${DICTFILE} ${TSLM_FILE3}
        DEPENDS tslmpack ${LM_SC_ARPA} ${DICTFILE})
    if (NOT EXISTS ${TSLM_INFO_FILE3})
        add_dependencies(tslmfile get_lm_sc)
    endif (NOT EXISTS ${TSLM_INFO_FILE3})
    if (NOT EXISTS ${DICTFILE})
        add_dependencies(lexicon get_dict)
    endif (NOT EXISTS ${DICTFILE})
endif (NOT TRAIN_LM)
