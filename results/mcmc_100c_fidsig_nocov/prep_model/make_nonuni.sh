#!/usr/bin/bash

cfname='nonuni_cmd.txt';
out_dir='./data/';
sf=10;
rn=2.2;
zn=0.21;
rk=2.6;
zk=0.63;
a=0.1;

rm $cfname

python make_nonuni.py $cfname $out_dir $sf $rn $zn $rk $zk $a
bash $cfname

# Add information about run
info_file='mock_info.txt';
rm $info_file
INFO="make_nonuni.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file