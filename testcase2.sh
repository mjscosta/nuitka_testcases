#!/bin/bash

TEST_CASE=2

echo "Nuitka testcase $TEST_CASE:"
echo "Context:"
echo "1- package with subpackages and submodules, one of them is a swig module."
echo "2- build recursively each .py module, except for swig modules."
echo "Result:"
echo "package result into dir: output$TEST_CASE"
echo "run main.py using PYTHONPATH=.../output$TEST_CASE"

mkdir build_swig
cd build_swig
cmake ../python_path_root/package1/subpackage3/swigpkg
make all
cd ..

mkdir output2
cp -r python_path_root/* output2

#./bin/nuitka_compile_modules.py --compile --clean-python --clean --recurse-none --root-dir output1

cd output2
nuitka --module ./package1

# delete the modules that will be replaced by nuitka, leave only the swig module.
rm -rf package1/subpackage1
rm -rf package1/subpackage2/
rm package1/*.py
rm -rf package1/packaging


#cd output2
#export PYTHONPATH=`pwd`
#cd ..

#echo "test main.py:"
#echo
#echo
#python main.py


