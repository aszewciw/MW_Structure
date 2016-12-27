#!/usr/bin/bash

cfname='mocks_cmd.txt';
out_dir='./mocks_data/';
nprocs=16;
nmocks=5;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python test_mocks.py $cfname $out_dir $nprocs $nmocks
bash $cfname

# Add information about run
info_file='mocks_info.txt';
rm $info_file
INFO="test_mocks.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file