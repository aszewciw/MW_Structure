#!/usr/bin/bash

cfname='nfc_cmd.txt';
in_dir='./data/';
ofname='nofrac_cov.dat'
nprocs=20;
max_s=100000;
frac=0;
cov=1;

rm $cfname
rm $ofname

python run_mcmc.py $cfname $in_dir $ofname $nprocs $max_s $frac $cov
bash $cfname

# Add information about run
info_file='nfc_info.txt';
rm $info_file
INFO="nofrac_cov.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file