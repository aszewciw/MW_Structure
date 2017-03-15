#!/usr/bin/bash

Nsamp=100;
Njk=10;
mock_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/;
out_dir=./data/;

python jk_mock.py $Nsamp $Njk $mock_dir $out_dir