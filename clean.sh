#!/bin/bash
rm -rf dist/ build/

find -maxdepth 1 -type d -name "build*"  -exec rm -rf {} \; -print
find -maxdepth 1 -type d -name "output*" -exec rm -rf {} \; -print
