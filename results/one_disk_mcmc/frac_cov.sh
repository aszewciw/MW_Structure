#!/usr/bin/bash

cfname='fc_cmd.txt';
in_dir='./data/';
ofname='frac_cov.dat';
nprocs=20;
max_s=100000;
frac=1;
cov=1;

rm $cfname
rm $ofname

python run_mcmc.py $cfname $in_dir $ofname $nprocs $max_s $frac $cov
bash $cfname

# Add information about run
info_file='fc_info.txt';
rm $info_file
INFO="frac_cov.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file