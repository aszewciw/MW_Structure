#!/usr/bin/bash

rm -rf ./mock_data
mkdir data

python test_mock.py

# Add information about run
info_file='mock_info.txt';
rm $info_file
INFO="test_mock.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file