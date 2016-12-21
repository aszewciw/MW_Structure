#!/usr/bin/bash

rm -rf ./data
mkdir data

python test_uniform.py

# Add information about run
info_file='uniform_info.txt';
rm $info_file
INFO="test_uniform.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file