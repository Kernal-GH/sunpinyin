#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").  
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at sunpinyin/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at sunpinyin/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Process this file with autoconf to produce a configure script.
AC_INIT(scim-sunpinyin, 2.0)
AC_CANONICAL_SYSTEM()
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR(src/sunpinyin_imengine.cpp)
AM_CONFIG_HEADER(config.h)
AM_CONDITIONAL(DEBUG, test "$enable-debug" = yes)

GETTEXT_PACKAGE=scim-sunpinyin
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [The gettext domain])

dnl Init gettext
ALL_LINGUAS="zh_CN"
AM_GLIB_GNU_GETTEXT
LTLIBINTL=
AC_SUBST(LTLIBINTL)

dnl-----------------------------------------------------------------------
dnl    --enable-debug
dnl-----------------------------------------------------------------------
AC_ARG_ENABLE([debug],
    AC_HELP_STRING([--enable-debug], [compile in debug mode (default no) ]),
    [DEBUGMODE="${enableval}"],
    [DEBUGMODE="no"])

if test "X$DEBUGMODE" = "Xyes" ; then
    AC_DEFINE(DEBUG, 1, [Define if you want to make for debugging.])
fi

AC_ARG_WITH([sunpinyin-datadir],
    AC_HELP_STRING([--with-sunpinyin-datadir=PATH],
                   [specify the directory where the lexicon data is installed]),
    [SUNPINYIN_DATADIR="${withval}"],
    [SUNPINYIN_DATADIR=""])
AC_SUBST(SUNPINYIN_DATADIR)

PKG_CHECK_MODULES(sunpinyin, [sunpinyin-2.0 >= 2.0])
PKG_CHECK_MODULES(sqlite3, [sqlite3 >= 3.0])

# Check SCIM
SCIM_VERSION=1.4.0
AC_SUBST(SCIM_VERSION)
PKG_CHECK_MODULES(SCIM,[scim >= $SCIM_VERSION])

# Check if we should build setup module
PKG_CHECK_MODULES(SCIM_GTKUTILS,[scim-gtkutils >= $SCIM_VERSION],
                                [SCIM_HAS_GTKUTILS=yes],
                                [SCIM_HAS_GTKUTILS=no])
    
# Set paths
SCIM_ICONDIR=`$PKG_CONFIG --variable=icondir scim`
SCIM_MODULEDIR=`$PKG_CONFIG --variable=moduledir scim`
SCIM_DATADIR=`$PKG_CONFIG --variable=scimdatadir scim`
SCIM_SUNPINYIN_DATADIR=$SCIM_DATADIR/sunpinyin
AC_SUBST(SCIM_ICONDIR)
AC_SUBST(SCIM_MODULEDIR)
AC_SUBST(SCIM_DATADIR)
AC_SUBST(SCIM_SUNPINYIN_DATADIR)

AC_PROG_CC
AC_PROG_CPP
AC_PROG_CXX
AC_PROG_INSTALL
AC_PROG_LIBTOOL
IT_PROG_INTLTOOL([0.35.0])

# Checks for libraries.

# Checks for header files.
AC_PATH_X
AC_HEADER_STDC

AC_OUTPUT(Makefile
          src/Makefile
          setup/Makefile
          po/Makefile.in)
