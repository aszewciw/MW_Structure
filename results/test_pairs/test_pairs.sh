#!/usr/bin/bash

cfname='pairs_cmd.txt';
out_dir='./pairs_data/'

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python make_bins.py $out_dir
python pair_count.py $cfname $out_dir
bash $cfname

# Add information about run
info_file='run_info.txt';
rm $info_file
INFO="test.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file