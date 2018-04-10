#!/bin/bash

TEST_CASE=3

echo "Nuitka testcase $TEST_CASE:"
echo "Context:"
echo "1- package with subpackages and submodules."
echo "2- build all packages and sub-packages into a single lib."
echo "Result:"
echo "package result into dir: output$TEST_CASE"
echo "run main3.py using PYTHONPATH=.../output$TEST_CASE"


OUTPUT_DIR=output$TEST_CASE
mkdir $OUTPUT_DIR
cp -r python_path_root3/* $OUTPUT_DIR

cd $OUTPUT_DIR
nuitka --module ./package1

# clean python code
rm -rf package1/


export PYTHONPATH=`pwd`
cd ..

#echo "test main3.py:"
#echo
#echo
python main3.py


