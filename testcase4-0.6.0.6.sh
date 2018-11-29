#!/bin/bash

TEST_CASE=4

echo "Nuitka testcase $TEST_CASE:"
echo "Context:"
echo "1- sub-package with subpackages and submodules, one of them is a swig module."
echo "2- build recursively each .py module, except for swig modules."
echo "Result:"
echo "package result into dir: output$TEST_CASE"
echo "run main.py using PYTHONPATH=.../output$TEST_CASE"

mkdir build_swig
cd build_swig

CMAKE_GENERATOR=""

case "$(uname -s)" in
    Linux* | Darwin* )
        CMAKE_GENERATOR='"Unix Makefiles"'
        ;;
    MINGW* | CYGWIN* )
        CMAKE_GENERATOR='"NMake Makefiles JOM"'
        ;;
    *)
        echo "Unknown OS/System. Unnsble to test."
esac

[ -z $CMAKE_GENERATOR ] && exit 1

cmake -G $CMAKE_GENERATOR ../python_path_root/package1/subpackage3/swigpkg/ -DCMAKE_BUILD_TYPE=Release
cmake --build . --target all

cd ..

OUTPUT_DIR=output$TEST_CASE
mkdir $OUTPUT_DIR
cp -r python_path_root/* $OUTPUT_DIR

cd $OUTPUT_DIR
nuitka --module package1/subpackage2 --recurse-directory=./package1/subpackage2 --output-dir=./package1/


# delete the modules that will be replaced by nuitka, leave only the swig module.

# delete all files except the .so from swig.
find package1/subpackage2 -type f | grep -v ".*(so|pyd)$" | xargs rm
find package1/subpackage2 -type d -empty -print # delete empty directories

export PYTHONPATH=`pwd`
cd ..

echo "test main.py:"
echo
echo
python main.py

