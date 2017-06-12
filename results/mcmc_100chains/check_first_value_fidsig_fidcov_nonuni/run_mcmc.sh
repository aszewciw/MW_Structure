#!/usr/bin/bash

cfname='mcmc_cmd.txt';
indir='/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_fidcov_nonuni/data';
datdir='../prep_data_samps/data/';
outdir='./out_data/';
nprocs=16;
max_s=2;
tol=0.0;
Ndata=100;
cov=1;

rm $cfname

python run_mcmc.py $cfname $indir $datdir $outdir $nprocs $max_s $tol $cov $Ndata
bash $cfname

# Add information about run
info_file='mcmc_info.txt';
rm $info_file
INFO="run_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file