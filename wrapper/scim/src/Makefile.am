noinst_HEADERS  	= imi_scimwin.h \
			  sunpinyin_imengine_config_keys.h \
			  sunpinyin_imengine.h \
			  sunpinyin_keycode.h \
			  sunpinyin_lookup_table.h \
			  sunpinyin_private.h \
			  sunpinyin_utils.h

# 
# 
# scim-sunpinyin

# input method module
#
moduledir            = @SCIM_MODULEDIR@/IMEngine
module_LTLIBRARIES   = sunpinyin.la

sunpinyin_la_SOURCES =  sunpinyin_utils.cpp \
		        imi_scimwin.cpp \
		        sunpinyin_imengine.cpp \
			sunpinyin_lookup_table.cpp

sunpinyin_la_CXXFLAGS   = @SCIM_CFLAGS@ \
                          -I$(top_builddir)/src \
                          -I$(SUNPINYIN_SRC_DIR) \
                          -I$(PINYIN_SRC_DIR) \
                          -I$(LEXICON_SRC_DIR) \
                          -I$(SLM_SRC_DIR) \
                          -DSUNPINYIN_USERDATA_DIR_PREFIX=\"$(SUNPINYIN_USERDATA_DIR_PREFIX)\" \
                          -DSCIM_ICONDIR=\"@SCIM_ICONDIR@\" \
                          -DSCIM_SUNPINYIN_LOCALEDIR=\"$(datadir)/locale\" \
                          -DSUNPINYIN_DATA_DIR=\"@SCIM_SUNPINYIN_DATADIR@\" \
                          -DSCIM_SUNPINYIN_ICON_FILE=\"@SCIM_ICONDIR@/sunpinyin_logo.xpm\" \
                          -DENABLE_DEBUG

sunpinyin_la_LDFLAGS	= -avoid-version \
		     	  -rpath $(moduledir) \
			  -module \
			  $(LIBTOOL_EXPORT_OPTIONS) \
			  @SCIM_LIBS@ \
			  @LTLIBINTL@

sunpinyin_la_LIBADD	 = libsunpinyin.la

