#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import cast, cdll, c_char_p, c_int, c_size_t, c_void_p
from ctypes.util import find_library
import sys

class ConvertError(Exception):
    pass

class DictType:
    TEXT,DATRIE = 0,1

class OpenCC:

    def __init__(self, config=None, verbose=True):
        self.libopencc = cdll.LoadLibrary(find_library('opencc'))
        self.libopencc.opencc_open.restype = c_void_p
        self.libopencc.opencc_convert_utf8.argtypes = [c_void_p, c_char_p, c_size_t]
        # for checking for the returned '-1' pointer in case opencc_convert() fails.
        # c_char_p always tries to convert the returned (char *) to a Python string,
        self.libopencc.opencc_convert_utf8.restype = c_void_p
        self.libopencc.opencc_close.argtypes = [c_void_p]
        self.libopencc.opencc_perror.argtypes = [c_char_p]
        self.libopencc.opencc_dict_load.argtypes = [c_void_p, c_char_p, c_int]

        self.libc = cdll.LoadLibrary(find_library('c'))
        self.libc.free.argtypes = [c_void_p]

        self.config = config
        self.verbose = verbose
        self.od = None

    def open(self):
        if self.config is None:
            self.od = self.libopencc.opencc_open(0)
        else:
            self.od = self.libopencc.opencc_open(c_char_p(self.config))

    def close(self):
        self.libopencc.opencc_close(self.od)
        self.od = None
                        
    def __enter__(self):
        if self.od:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __perror(self, message):
        if self.verbose:
            self.libopencc.opencc_perror(message)
    
    def convert(self, text):
        '''text - unicode string

        N.B. because Python unicode string could be using UCS-2 or UCS-4 upon
        its configuration, if the input/out is in non-BMP (CJK Unified
        Ideographs Extension B/C/D), the result of converting could be unexpected
        on Python configured with UCS-2 unicode string.
        '''
        assert isinstance(text, unicode), '"text" should be an unicode string'
        # XXX: we may don't need to convert a python unicode string to utf-8
        # and back by adding opencc_convert_wchar() where a wchar_t is 4
        # bytes long and the string is encoded in UCS-4.
        # the only caveat is that we can not assume the size of wchar_t on
        # all platform.
        text = text.encode('utf-8')
        retv_c = self.libopencc.opencc_convert_utf8(self.od, text, len(text))
        if retv_c == -1:
            self.__perror('OpenCC error:')
            raise ConvertError()
        retv_c = cast(retv_c, c_char_p)
        str_buffer = retv_c.value
        self.libc.free(retv_c)
        return unicode(str_buffer, 'utf-8')
    
    def dict_load(self, filename, dicttype):
        retv = self.libopencc.opencc_dict_load(self.od, filename, dicttype)
        if retv == -1:
            self.__perror('OpenCC error:')
        return retv



import sunpinyin

the_opencc = None
@sunpinyin.register.translator
def opencc(text):
    global the_opencc
    if the_opencc is None:
        the_opencc = OpenCC()
        the_opencc.open()
        for path in ['simp_to_trad_characters.ocd',
                     'simp_to_trad_phrases.ocd']:
            the_opencc.dict_load(path, DictType.DATRIE)
    result = the_opencc.convert(text)
    return result

if __name__ == "__main__":
    with sys.stdin as fp:
        text = fp.read()
    with OpenCC() as converter:
        for path in ['simp_to_trad_characters.ocd',
                 'simp_to_trad_phrases.ocd']:
            converter.dict_load(path, DictType.DATRIE)
        print converter.convert(text)
