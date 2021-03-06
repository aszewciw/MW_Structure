#!/usr/bin/bash

cfname='mocks_cmd.txt';
out_dir='./data/';
nprocs=16;
nmocks=1000;
rn=2.3;
zn=0.25;
rk=2.5;
zk=0.63;
a=0.08;

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