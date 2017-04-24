#!/usr/bin/env bash

set -e

mkdir build && cd build && cmake .. && make && cd ..
mkdir -p results/{filtered,sorted,sorted_each,transformations_build,nearest_neighbours,acyclic_graph}
