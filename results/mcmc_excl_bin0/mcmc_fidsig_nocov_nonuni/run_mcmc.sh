#!/usr/bin/bash

cfname=mcmc_cmd.txt;
indir=./data/;
datdir=/fs1/szewciw/MW_Structure/results/mcmc_100chains/prep_data_samps/data/sample_0/;
outdir=./out_data/;
nprocs=20
max_s=500000;
tol=0.0;

rm $cfname

python run_mcmc.py $cfname $indir $datdir $outdir $nprocs $max_s $tol
bash $cfname

# Add information about run
info_file=mcmc_info.txt;
rm $info_file
INFO="run_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file