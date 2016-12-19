#!/usr/bin/bash

# Pass this directory as an argument
# Compiled executable will be output to binary dir within working dir
CUR_DIR=$1

icc -Wall -xHost -O3 -vec_report2 -openmp $1pair_count_openmp.c -o ./bin/pair_count_openmp
