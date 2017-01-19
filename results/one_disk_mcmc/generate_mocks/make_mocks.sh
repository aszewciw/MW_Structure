#!/usr/bin/bash

cfname='mocks_cmd.txt';
out_dir='./data/';
nprocs=16;
nmocks=5;
rn=2.6;
zn=0.27;
a=0.0;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python make_mocks.py $cfname $out_dir $nprocs $nmocks $rn $zn $a
bash $cfname

# Add information about run
info_file='mocks_info.txt';
rm $info_file
INFO="make_mocks.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file