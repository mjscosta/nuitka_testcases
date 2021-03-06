#!/bin/bash

set -xv

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

CMAKE_GENERATOR=""

case "$(uname -s)" in
    Linux* | Darwin* )
        CMAKE_GENERATOR='Unix Makefiles'
        cmake -G "$CMAKE_GENERATOR" ../python_path_root/package1/subpackage3/swigpkg/ -DCMAKE_BUILD_TYPE=Release
        cmake --build . --target all
        ;;
    MINGW* | CYGWIN* )
        CMAKE_GENERATOR='NMake Makefiles JOM'
        WIN_PWD=$(cmd //C cd)
        cmd //C call 'C:\Program Files (x86)\Microsoft Visual C++ Build Tools\vcbuildtools.bat' amd64 \& cd $WIN_PWD \& \
        cmake -G "$CMAKE_GENERATOR" '..\python_path_root\package1\subpackage3\swigpkg\' -DCMAKE_BUILD_TYPE=Release \& \
        cmake --build . --target all
        ;;
    *)
        echo "Unknown OS/System. Unnsble to test."
esac

[[ -z $CMAKE_GENERATOR ]] && exit 1

echo $CMAKE_GENERATOR

cd ..

OUTPUT_DIR=output$TEST_CASE
mkdir $OUTPUT_DIR
cp -r python_path_root/* $OUTPUT_DIR

cd $OUTPUT_DIR

nuitka --module --include-package=package1 --recurse-to=package1 --recurse-not-to=package1.subpackage3.swigpkg ./package1


# delete the modules that will be replaced by nuitka, leave only the swig module.
rm -rf package1/subpackage1
rm -rf package1/subpackage2
rm -rf package1/packaging
rm package1/*.py

# delete all files except the .so from swig.
find package1 -type d -name __pycache__ -delete -print
find package1 -maxdepth 2 -type f | grep -vP ".*(so|pyd|manifest)$" | xargs rm

export PYTHONPATH=`pwd`
cd ..

echo "test main.py:"
echo
echo
python main.py


