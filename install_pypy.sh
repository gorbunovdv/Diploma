#!/usr/bin/env bash

set -e

git clone https://bitbucket.org/pypy/numpy.git;
cd numpy
python setup.py install
cd ..
