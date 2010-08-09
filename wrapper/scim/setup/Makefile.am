SETUP_MODULE = sunpinyin-imengine-setup.la
setupmoduledir           = @SCIM_MODULEDIR@/SetupUI
setupmodule_LTLIBRARIES  = $(SETUP_MODULE)

sunpinyin_imengine_setup_la_SOURCES = sunpinyin_imengine_setup.cpp

sunpinyin_imengine_setup_la_CXXFLAGS= @SCIM_GTKUTILS_CFLAGS@ \
                                   @SCIM_CFLAGS@ \
			  	   -DSCIM_SUNPINYIN_LOCALEDIR=\"$(datadir)/locale\"

sunpinyin_imengine_setup_la_LDFLAGS = -avoid-version \
                                      -rpath $(setupmoduledir) \
                                      -module \
                                      $(LIBTOOL_EXPORT_OPTIONS) \
                                      @SCIM_GTKUTILS_LIBS@ \
                                      @LTLIBINTL@ \
                                      @SCIM_LIBS@

icondir                  = $(SCIM_ICONDIR)
icon_DATA                = $(top_builddir)/data/sunpinyin_logo.xpm
