#!/usr/bin/bash

cfname='mock_cmd.txt';
out_dir='./data/';
a=0.0;

rm $cfname

python make_mock.py $cfname $out_dir $a
bash $cfname

# Add information about run
info_file='mock_info.txt';
rm $info_file
INFO="make_mock.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file