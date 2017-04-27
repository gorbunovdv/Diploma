#!/usr/bin/env bash

set -e
sudo apt-get update
sudo apt-get install htop g++ git aptitude cmake python libjemalloc-dev python-pip p7zip-full unzip virtualenvwrapper pypy pypy-dev
pip install numpy pathos
