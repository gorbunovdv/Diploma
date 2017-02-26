sudo apt-get install htop g++ git aptitude cmake python
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp && cmake . && make -j4 && sudo make install && cd ..
mkdir build && cd build && cmake .. && make && cd ..