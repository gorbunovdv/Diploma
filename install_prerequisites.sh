#!/usr/bin/env bash

set -e
sudo apt-get update
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt-get install htop g++ git aptitude cmake python libjemalloc-dev python-pip p7zip-full unzip
pip install numpy pathos gensim

bash install_jsoncpp.sh