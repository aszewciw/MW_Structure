#!/usr/bin/bash

cfname='mocks_cmd.txt';
out_dir='./data/';
nprocs=12;
nmocks=1000;
rn=69.627;
zn=0.259;
rk=4.881;
zk=0.691;
a=0.736;

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