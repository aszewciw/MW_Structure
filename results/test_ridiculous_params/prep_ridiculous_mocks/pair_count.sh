#!/usr/bin/bash

cfname='pairs_cmd.txt';
mocks_dir='./data/';
out_dir='./data/';
bins_dir='/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_bins/';
Nmocks=1000;

rm $cfname

python pair_count.py $cfname $mocks_dir $out_dir $bins_dir $Nmocks
bash $cfname

# Add information about run
info_file='pairs_info.txt';
rm $info_file
INFO="pair_count.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file