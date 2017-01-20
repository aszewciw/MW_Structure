#!/usr/bin/bash

cfname='pairs_cmd.txt';
out_dir='./data/';
mocks_dir='../generate_mocks/data/';
Nmocks=1000;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python make_bins.py $out_dir
python pair_count.py $cfname $mocks_dir $out_dir $Nmocks
bash $cfname

# Add information about run
info_file='pairs_info.txt';
rm $info_file
INFO="pair_count.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file