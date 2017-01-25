#!/usr/bin/bash

cfname='mcmc_cmd.txt';
indir='./data/';
datdir='./prep_data_samps/data/';
outdir='./out_data/';
nprocs=16;
max_s=100000;
tol=0.0;
Ndata=1;

rm $cfname

python run_mcmc.py $cfname $indir $datdir $outdir $nprocs $max_s $tol $Ndata
bash $cfname

# Add information about run
info_file='mcmc_info.txt';
rm $info_file
INFO="run_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file