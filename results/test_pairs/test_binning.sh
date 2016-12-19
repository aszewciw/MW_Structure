#!/usr/bin/bash

rm -rf ./data
mkdir data

python make_bins.py
time python bin_pair_indices.py

# Add information about run
info_file='run_info.txt';
rm $info_file
INFO="test_binning.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file