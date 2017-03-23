#!/usr/bin/bash

N_mocks=10000;
pairs_dir=/fs1/szewciw/MW_Structure/results/error_analysis/data_pairs/;
out_dir=./plots/;
bins_dir=../prep_bins/;

rm -rf $out_dir
mkdir $out_dir

python check_gaussianity.py $N_mocks $pairs_dir $out_dir $bins_dir