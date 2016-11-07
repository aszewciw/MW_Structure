#!/usr/bin/bash

rm -rf ./data_omp
mkdir data_omp

if [[ $# -ne 1 ]] ; then
    echo "usage: ./pair_count_openmp num_threads"
    exit 1
fi
export OMP_NUM_THREADS=$1

python make_bins.py
time python pair_count_openmp.py

# Add information about run
info_file='run_info_omp.txt';
rm $info_file
INFO="test_omp.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file