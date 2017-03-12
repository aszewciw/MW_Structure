#!/usr/bin/bash

cfname='mock_cmd.txt';
out_dir='./mock_data/';

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python test_mock.py $cfname $out_dir
bash $cfname

# Add information about run
info_file='mock_info.txt';
rm $info_file
INFO="test_mock.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file