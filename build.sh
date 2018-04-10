#!/bin/bash

mkdir build_swig
cd build_swig
cmake ../python_path_root/package1/subpackage3/swigpkg
make all


pyinstaller -y main.spec
