#!/usr/bin/env python
"""
setup.py for Transience

To update the version number : 
vim -o transience/__init__.py
"""
from setuptools import setup
import sys
import transience

setup(
    name="transience",
    version=transience.__version__,
    description="Python interface to jack audio connection kit",
    author="Michal Seta",
    author_email="djiamnot@gmail.com",
    url="http://github.com/djiamnot/transience",
    packages=['transience'],
    scripts=[]
    )
