#!/usr/bin/bash

N_jk=10;
mock_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/sample_0/;
out_dir=./data/;

python jk_mock.py $N_jk $mock_dir $out_dir