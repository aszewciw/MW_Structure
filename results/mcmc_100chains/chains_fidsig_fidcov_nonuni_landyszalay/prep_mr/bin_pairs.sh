#!/usr/bin/bash

cfname=binned_cmd.txt;
out_dir=./data/;
bins_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_bins/;
model_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_model_nonuniform/data/;
rand_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_randoms/data/;

rm $cfname
rm -rf $out_dir
mkdir $out_dir

python bin_pairs.py $cfname $out_dir $bins_dir $model_dir $rand_dir
bash $cfname

# Add information about run
info_file=binned_info.txt;
rm $info_file
INFO="bin_pairs.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file