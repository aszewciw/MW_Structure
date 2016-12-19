#!/usr/bin/bash

# Pass source code (i.e. this) directory as an argument
# Compiled executable will be output to binary dir within working dir
CUR_DIR=$1

icc -Wall -xHost -O3 -vec_report2 $1pair_count.c -o ./bin/pair_count