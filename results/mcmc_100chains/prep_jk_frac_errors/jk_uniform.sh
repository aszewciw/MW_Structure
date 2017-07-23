#!/usr/bin/bash

Njk=10;
uni_dir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_model_uniform/data/;
out_dir=./data_uniform/;

python jk_uniform.py $Njk $uni_dir $out_dir