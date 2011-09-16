#!/bin/bash

export VERSIONER_PYTHON_PREFER_32BIT=yes
rm -fr build/ dist/
python setup_darwin.py py2app
