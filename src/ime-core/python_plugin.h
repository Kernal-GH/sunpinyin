#ifndef SUNPY_PY_PLUGINS
#define SUNPY_PY_PLUGINS

#include <vector>
#include <portability.h>

#include <Python.h>


class PyPlugins
{
public:
    PyPlugins();
    ~PyPlugins();

	operator bool() const;
	bool init();
	void fini();
    
    wstring trans(const wstring& text);
    wstring abbre(const wstring& spell);
    
private:
	wstring call(PyObject* method, const wstring& str);
    
private:
    PyObject* m_module;
    PyObject* m_plugins;
    PyObject* m_tran_method_name;
    PyObject* m_abbr_method_name;
};


#endif //SUNPY_PY_PLUGINS
