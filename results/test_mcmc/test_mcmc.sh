#!/usr/bin/bash

cfname='mcmc_cmd.txt';
in_dir='./data/';
ofname='mcmc_result.dat'
nprocs=16;
max_s=500000;
tol=0.0;

rm $cfname
rm $ofname

python test_mcmc.py $cfname $in_dir $ofname $nprocs $max_s $tol
bash $cfname

# Add information about run
info_file='mcmc_info.txt';
rm $info_file
INFO="test_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file