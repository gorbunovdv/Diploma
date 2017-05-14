#!/usr/bin/env bash

set -e
git clone https://github.com/svn2github/word2vec.git

cd word2vec
make

cd ..
./word2vec/word2vec -train $1 -min-count 0 -save-vocab vectors.vocab
./word2vec/word2vec -train $1 -output vectors.bin -cbow 1 -size 100 -window 10 -negative 10 -hs 0 -sample 1e-5 -threads 10 -binary 1 -iter 3 -min-count 10
