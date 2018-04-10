#!/bin/bash

echo "Nuitka testcase 1:"
echo "Context:"
echo "1- package with subpackages and submodules, one of them is a swig module."
echo "2- build recursively each .py module, except for swig modules."
echo "Result:"
echo "package result into dir: output1"
echo "run main.py using PYTHONPATH=.../output1"

mkdir build_swig
cd build_swig
cmake ../python_path_root/package1/subpackage3/swigpkg
make all
cd ..

mkdir output1
cp -r python_path_root/* output1

./bin/nuitka_compile_modules.py --compile --clean-python --clean --recurse-none --root-dir output1

cd output1
export PYTHONPATH=`pwd`
cd ..

echo "test main.py:"
echo
echo
python main.py


