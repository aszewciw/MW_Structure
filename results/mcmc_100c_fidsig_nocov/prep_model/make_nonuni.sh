#!/usr/bin/bash

cfname='nonuni_cmd.txt';
out_dir='./data/';
sf=10;

rm $cfname

python make_nonuni.py $cfname $out_dir $sf
bash $cfname

# Add information about run
info_file='mock_info.txt';
rm $info_file
INFO="make_nonuni.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file