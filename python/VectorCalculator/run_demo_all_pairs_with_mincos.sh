#!/usr/bin/env bash

rm corpus_en.norm-sz100-w3-cb0-it1-min20.w2v
wget https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/en/corpus_en.norm-sz100-w3-cb0-it1-min20.w2v
echo "{\"model\":\"corpus_en.norm-sz100-w3-cb0-it1-min20.w2v\"}" > config.json || exit
python main_all_pairs_with_mincos.py || exit
