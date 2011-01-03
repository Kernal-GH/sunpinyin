#include <cassert>
#include <climits>		// for PATH_MAX
#include <iostream>
#include <stdexcept>

#include "python_utils.h"

using namespace std;

PyPlugins::PyPlugins() {
    Py_Initialize();
    if (!Py_IsInitialized()) {
	  throw runtime_error("failed to initialize  runtime");
    }
}

PyPlugins::~PyPlugins() {
}

PyPlugins::operator bool() const {
    return !!m_plugins;
}

bool
PyPlugins::init() {
    PyRun_SimpleString("import sys");
	
    char path[PATH_MAX];
    const char* home = getenv("HOME");
    snprintf(path, sizeof(path), "%s/%s", home, ".sunpinyin/plugins");

    char py_stmt[PATH_MAX];
    int len = snprintf(py_stmt, sizeof(py_stmt),
		       "if '%s' not in sys.path: "
		       "sys.path.append('%s')",
		       path, path);
    assert(len < sizeof(py_stmt) && "py_stmt truncated.");
    PyRun_SimpleString(py_stmt);
	PyObject* load_result = 0;
    if ( (m_module = PyImport_ImportModule("sunpinyin")) != NULL &&
		 (m_plugins = PyObject_GetAttrString(m_module, "plugins")) != NULL &&
		 (load_result = PyObject_CallMethod(m_plugins, "load", NULL)) != NULL) {
		if (PyObject_IsTrue(load_result) == 0) {
			// no plugin is loaded
			return false;
		} else {
			Py_XDECREF(load_result);
		}
		m_tran_method_name = PyString_FromString("do_tran");
		m_abbr_method_name = PyString_FromString("do_abbr");
		return true;
    } else {
		cout << "faild to initialize python plugins" << endl;
		return false;
    }
}

void
PyPlugins::fini() {
    Py_XDECREF(m_tran_method_name);
    Py_XDECREF(m_abbr_method_name);
    Py_XDECREF(m_plugins);
    Py_XDECREF(m_module);
}
    
wstring
PyPlugins::trans(const wstring& text) {
    return call(m_tran_method_name, text);
}

wstring
PyPlugins::abbre(const wstring& spell) {
    return call(m_abbr_method_name, spell);
}
    
wstring
PyPlugins::call(PyObject* method, const wstring& str) {
    PyObject* src = PyUnicode_FromWideChar(str.c_str(), str.size());
    PyObject* result = PyObject_CallMethodObjArgs(m_plugins,
												  method,
												  src, NULL);
    Py_CLEAR(src);

	if (result == NULL) {
		cerr << "failed to call plugin method" << endl;
		PyErr_Print();
		return str;
	}
    wstring out(str.size(), L' ');
    int len = PyUnicode_AsWideChar((PyUnicodeObject*)result, &out[0], out.size());
	Py_CLEAR(result);
	if (len == -1) {
		cerr << "bad plugin. fall back to original str" << endl;
		return str;
	}
    if (len < out.size()) {
		out.resize(len);
    }
    return out;
}
