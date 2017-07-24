#!/usr/bin/bash

Nsamp=100;
N_jk=10;
bins_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_bins/;
jk_dir=./data_mocks/;
out_dir=./data_mocks/;

python jk_err_mocks.py $N_jk $bins_dir $jk_dir $out_dir $Nsamp