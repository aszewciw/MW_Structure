#!/usr/bin/bash

cfname=dr_cmd.txt;
out_dir=./data/;
bins_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_bins/;
data_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/;
rand_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_randoms/data/;
Nmocks=1;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python dr_counts.py $cfname $out_dir $bins_dir $data_dir $rand_dir $Nmocks
bash $cfname

# Add information about run
info_file=dr_info.txt;
rm $info_file
INFO="dr_counts.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file