#!/usr/bin/bash

cfname='mocks_cmd.txt';
out_dir='./data/';
nprocs=16;
nmocks=100;
rn=2.55;
zn=0.225;
rk=2.50;
zk=0.653;
a=0.098;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python make_mocks.py $cfname $out_dir $nprocs $nmocks $rn $zn $rk $zk $a
bash $cfname

# Add information about run
info_file='mocks_info.txt';
rm $info_file
INFO="make_mocks.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file