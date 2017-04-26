#!/usr/bin/env bash

set -e

mkvirtualenv pypy-diploma -p /usr/bin/pypy
git clone https://bitbucket.org/pypy/numpy.git;
cd numpy
python setup.py install
cd ..
