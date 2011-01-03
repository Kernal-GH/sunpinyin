#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from collections import OrderedDict       # XXX: python 2.7 only

params = dict(level=logging.DEBUG,
              format="%(asctime)s - %(levelname)s: %(message)s")
if __name__ == '__main__':
    params['stream'] = sys.stderr
else:
    params['filename'] = 'plugin.log'
    params['filemode'] = 'w'

logging.basicConfig(**params)

class Plugins(object):
    def __init__(self):
        self.trans = OrderedDict()
        self.abbrs = OrderedDict()

    def translator(self, func):
        name = func.__name__
        if name in self.trans:
            logging.info('translator plugin "%s" already registered, '
                         'replacing it.' % name)
        logging.debug('translator plugin "%s" registered' % name)
        self.trans[name] = func
        return func

    def abbrev(self, func):
        name = func.__name__
        if name in self.abbrs:
            logging.info('abbrev plugin "%s" already registered, '
                         'replacing it.' % name)
        logging.debug('abbrev plugin "%s" registered' % name)
        self.abbrs[name] = func
        return func

    def do_tran(self, text):
        for name, tran in self.trans.iteritems():
            result = tran(text)
            logging.debug('%s(%s) => %s' % (name, text, result))
            text = result
        return text

    def do_abbr(self, spell):
        result = None
        for name, abbr in self.abbrs.iteritems():
            result = abbr(spell)
            logging.debug('%s(%s) => %r' % (name, spell, result))
            if result is not None:
                break
        return result

    def load(self, force=False):
        '''load plugins in system and user plugin directories in turn
        
        reset existing plugin chains before appending plugins to them.
        '''
        if self.trans or self.abbrs:
            if not force:
                return
            self.trans.clear()
            self.abbrs.clear()
    
        plugin_paths = ['/usr/local/lib/sunpinyin/plugins',
                        '/usr/lib/sunpinyin/plugins',
                        os.path.expanduser('~/.sunpinyin/plugins')]
        if sys.platform == 'darwin':
            plugin_paths.append('/Library/Input\ Methods/'
                                'SunPinyin.app/Contents/Resources/'
                                'plugins')
        for path in plugin_paths:
            if not os.path.exists(path):
                continue
            if path not in sys.path:
                sys.path.append(path)
            for f in sorted(os.listdir(path)):
                # N.B. user should name her plugin carefully so that they are
                # registered in the expected order.
                fn, ext = os.path.splitext(f)
                if fn == 'sunpinyin' or ext != '.py':
                    continue
                try:
                    logging.debug('loading %s' % fn)
                    if fn in sys.modules:
                        reload(sys.modules[fn])
                    else:
                        __import__(fn, globals(), locals(), [], -1)
                except Exception as e:
                    logging.error('failed to load plugin: %s/%s (%r)' % (path, fn, e))
        logging.info('%d tran plugins loaded' % len(self.trans))
        logging.info('%d abbr plugins loaded' % len(self.abbrs))
        return True if self.trans or self.abbrs else False

register = plugins = Plugins()
# should not call plugins.load() in this file, it will possibly load plugins
# which in turn imports sunpinyin _again_ while it is actually being loaded.
# so, in this case, the `register` in the outer round of loading is different
# from `register` in the inner round of loading.
# in other words, the `register` variable from plugin's point of view is not
# `sunpinyin.register` after loading completes -- we always end up with a
# empty `plugins` in this way.

if __name__ == '__main__':
    plugins.load()
    print plugins.do_trans('开放中文转换')

