#!/usr/bin/env bash

set -e
sudo apt-get update
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt-get install htop g++ git aptitude cmake python libjemalloc-dev python-pip p7zip-full
pip install numpy pathos gensim
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp && cmake . && make -j4 && sudo make install && cd ..
mkdir build && cd build && cmake .. && make && cd ..
mkdir -p results/{filtered,sorted,sorted_each,transformations_build,nearest_neighbours,acyclic_graph}
