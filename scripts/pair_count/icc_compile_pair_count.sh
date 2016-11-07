#!/usr/bin/bash

# Pass source code (i.e. this) directory as an argument
# Compiled executable will be output to wherever working directory is
CUR_DIR=$1

icc -Wall -xHost -O3 -vec_report2 $1pair_count.c -o pair_count