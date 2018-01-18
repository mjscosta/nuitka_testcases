#include "myswig_module.h"
#include <iostream>


myswig_module::myswig_module() {}
myswig_module::~myswig_module() {}

void myswig_module::print_myswig_module(PyObject * var) {
    PyObject* objectsRepresentation = PyObject_Repr(var);
    const char* s = PyString_AsString(objectsRepresentation);
    std::cout << "swig_module: " << s << std::endl;
}
