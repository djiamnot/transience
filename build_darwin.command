#!/bin/bash

export VERSIONER_PYTHON_PREFER_32BIT=yes
rm -fr build/ dist/
python setup_darwin.py py2app
# compensate for broken py2app no capable of copying loadable data to site-packages.zip!
unzip dist/Transience.app/Contents/Resources/lib/python2.7/site-packages.zip -d dist/Transience.app/Contents/Resources/lib/python2.7/site-packages
cp -r media dist/Transience.app/Contents/Resources/lib/python2.7/site-packages
cd dist/Transience.app/Contents/Resources/lib/python2.7/
rm site-packages.zip
zip -r site-packages site-packages/
rm -fr site-packages
