sudo apt-get install htop g++ git aptitude cmake python libjemalloc-dev
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp && cmake . && make -j4 && sudo make install && cd ..
mkdir build && cd build && cmake .. && make && cd ..
mkdir -p results/{filtered,sorted,sorted_each,transformations_build}
wget https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/en/corpus_en.norm-sz100-w8-cb0-it1-min20.w2v
