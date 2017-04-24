#!/usr/bin/env bash

set -e
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp && cmake . && make -j4 && sudo make install && cd ..
