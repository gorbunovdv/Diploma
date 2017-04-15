#!/usr/bin/env bash

sudo apt-get update
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt-get install htop g++ git aptitude cmake python libjemalloc-dev python-pip p7zip-full
pip install numpy pathos gensim
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp && cmake . && make -j4 && sudo make install && cd ..
mkdir build && cd build && cmake .. && make && cd ..
mkdir -p results/{filtered,sorted,sorted_each,transformations_build}
wget https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/en/corpus_en.norm-sz100-w8-cb0-it1-min20.w2v
