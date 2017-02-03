#!/usr/bin/bash

cfname='errors_cmd.txt';
pairs_dir='./data/';
out_dir='./errors_data/';
Nmocks=1000;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python calc_errors.py $cfname $pairs_dir $out_dir $Nmocks
bash $cfname

# Add information about run
info_file='errors_info.txt';
rm $info_file
INFO="calc_errors.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file