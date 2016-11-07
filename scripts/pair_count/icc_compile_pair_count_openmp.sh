#!/usr/bin/bash

# Pass this directory as an argument
# Compiled executable will be output to wherever working directory is
CUR_DIR=$1

rm $1pair_count

gcc -Wall -O3 $1pair_count.c -o pair_count