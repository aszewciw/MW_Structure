#!/usr/bin/bash

cfname='uniform_cmd.txt';
out_dir='./uniform_data/';
num_ratio=10; # N_uniform / N_data

rm -rf $out_dir
mkdir $out_dir

python test_uniform.py $cfname $out_dir $num_ratio
bash $cfname

# Add information about run
info_file='uniform_info.txt';
rm $info_file
INFO="test_uniform.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file