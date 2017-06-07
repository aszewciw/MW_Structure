#!/usr/bin/bash

# Pass source code (i.e. this) directory as an argument
# Compiled executable will be output to binary dir within working dir
CUR_DIR=$1

gcc -Wall -O3 $1cross_pair_count.c -o ./bin/cross_pair_count