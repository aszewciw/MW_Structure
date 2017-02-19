#!/usr/bin/bash

cfname='mcmc_cmd_alt.txt';
indir='./data/';
datdir='../prep_data_samps_bestfit/data/';
outdir='./out_data/';
nprocs=16;
max_s=100000;
tol=0.0;
Ndata=100;
rn=2.55;
zn=0.225;
rk=2.50;
zk=0.653;
a=0.098;

rm $cfname

python run_mcmc.py $cfname $indir $datdir $outdir $nprocs $max_s $tol $Ndata \
$rn $zn $rk $zk $a
bash $cfname

# Add information about run
info_file='mcmc_info_alt.txt';
rm $info_file
INFO="run_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file