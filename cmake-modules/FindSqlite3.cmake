# Locate Sqlite3
# This module defines
# SQLITE3_LIBRARY
# SQLITE3_FOUND, if false, do not try to link to Sqlite3
# SQLITE3_INCLUDE_DIR, where to find the headers

FIND_PATH(SQLITE3_INCLUDE_DIR sqlite3.h
    HINTS
    $ENV{SQLITE3_DIR}
    PATH_SUFFIXES include
    PATHS
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local
    /usr
    /sw # Fink
    /opt/local # DarwinPorts
    /opt/csw # Blastwave
    /opt
    /usr/freeware
)

FIND_LIBRARY(SQLITE3_LIBRARY
    NAMES sqlite3 libsqlite3
    HINTS
    $ENV{SQLITE3_DIR}
    PATH_SUFFIXES lib lib64
    PATHS
    ~/Library/Frameworks
    /Library/Frameworks
    /usr/local
    /usr
    /sw
    /opt/local
    /opt/csw
    /opt
    /usr/freeware
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Sqlite3 DEFAULT_MSG SQLITE3_LIBRARY SQLITE3_INCLUDE_DIR)
MARK_AS_ADVANCED(SQLITE3_LIBRARY SQLITE3_INCLUDE_DIR)



