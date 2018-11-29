#include "myswig_module.h"
#include <iostream>


myswig_module::myswig_module() {}
myswig_module::~myswig_module() {}

void myswig_module::print_myswig_module(PyObject * var) {
    if (PyUnicode_Check(var)) {
        PyObject * temp_bytes = PyUnicode_AsEncodedString(var, "UTF-8", "strict"); // Owned reference
        if (temp_bytes != NULL) {
            char* s = PyBytes_AS_STRING(temp_bytes); // Borrowed pointer
            std::cout << "swig_module: " << s << std::endl;
            Py_DECREF(temp_bytes);
        } else {
            std::cout << "some error: " << std::endl;
        }
    } else if (PyBytes_Check(var)) {
            char* s = PyBytes_AS_STRING(var); // Borrowed pointer
            std::cout << "swig_module: " << s << std::endl;
    } else {
        std::cout << "some error: " << std::endl;
    }
}
