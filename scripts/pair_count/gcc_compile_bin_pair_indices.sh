#!/usr/bin/bash

# Pass source code (i.e. this) directory as an argument
# Compiled executable will be output to binary dir within working dir
CUR_DIR=$1

gcc -Wall -O3 $1bin_pair_indices.c -o ./bin/bin_pair_indices