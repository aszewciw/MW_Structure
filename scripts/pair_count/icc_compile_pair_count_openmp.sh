#!/usr/bin/bash

# Pass this directory as an argument
# Compiled executable will be output to wherever working directory is
CUR_DIR=$1

icc -Wall -xHost -O3 -vec_report2 -openmp $1pair_count_openmp.c -o pair_count_openmp
