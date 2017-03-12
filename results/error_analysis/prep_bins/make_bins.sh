#!/usr/bin/bash

cfname='bins_cmd.txt';
out_dir='./';
Nmocks=100;

rm $cfname

python make_bins.py $out_dir
bash $cfname

# Add information about run
info_file='bins_info.txt';
rm $info_file
INFO="make_bins.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file