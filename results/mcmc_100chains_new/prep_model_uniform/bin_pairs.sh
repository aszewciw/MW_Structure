#!/usr/bin/bash

cfname='binned_cmd.txt';
out_dir='./data/';
bins_dir='../prep_bins/';

rm $cfname

python bin_pairs.py $cfname $out_dir $bins_dir
bash $cfname

# Add information about run
info_file='binned_info.txt';
rm $info_file
INFO="bin_pairs.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file