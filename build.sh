#!/bin/bash

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

pyinstaller -y main.spec
