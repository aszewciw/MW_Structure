#!/usr/bin/bash

N_jk=10;
bins_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_bins/;
jk_dir=./data/;
out_dir=./data/;

python jk_errors.py $N_jk $bins_dir $jk_dir $out_dir