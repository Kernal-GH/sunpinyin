#ifndef SUNPY_IMI_PYTHON_UTILS
#define SUNPY_IMI_PYTHON_UTILS

#include <vector>
#include <string>

#include <Python.h>


class PyPlugins
{
public:
    PyPlugins();
    ~PyPlugins();

	operator bool() const;
	bool init();
	void fini();
    
    std::wstring trans(const std::wstring& text);
    std::wstring abbre(const std::wstring& spell);
    
private:
	std::wstring call(PyObject* method, const std::wstring& str);
    
private:
    PyObject* m_module;
    PyObject* m_plugins;
    PyObject* m_tran_method_name;
    PyObject* m_abbr_method_name;
};


#endif //SUNPY_IMI_PYTHON_UTILS
