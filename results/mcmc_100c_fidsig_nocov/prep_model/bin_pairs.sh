#!/usr/bin/bash

cfname='binned_cmd.txt';
out_dir='../data/';

rm $cfname

python make_bins.py $out_dir
python bin_pair_indices.py $cfname $out_dir
bash $cfname

# Add information about run
info_file='binned_info.txt';
rm $info_file
INFO="bin_pairs.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file