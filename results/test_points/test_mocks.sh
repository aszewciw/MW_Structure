#!/usr/bin/bash

rm -rf ./mocks_data
mkdir mocks_data

python test_mocks.py
bash mocks_cmd.txt

# Add information about run
info_file='mocks_info.txt';
rm $info_file
INFO="test_mocks.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file