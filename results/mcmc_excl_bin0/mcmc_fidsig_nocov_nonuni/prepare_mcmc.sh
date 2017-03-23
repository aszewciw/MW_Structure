#!/usr/bin/bash

chains_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains;

out_dir=./data/;
data_dir=$chains_dir/prep_data_samps/data/sample_0/;
model_dir=$chains_dir/prep_model_nonuniform/data/;
stats_dir=$chains_dir/prep_fid_errors/errors_data/;
fid_dir=$chains_dir/prep_fid_errors/errors_data/;
bins_dir=$chains_dir/prep_bins/;


python prepare_mcmc.py $out_dir $data_dir $model_dir $stats_dir $fid_dir $bins_dir

# Add information about run
info_file=prep_info.txt;
rm $info_file
INFO="prepare_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file