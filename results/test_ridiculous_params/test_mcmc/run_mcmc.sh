#!/usr/bin/bash

cfname='mcmc_cmd.txt';
indir='/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_fidcov_nonuni/data/';
datdir='./data/';
ofname='results.dat';
nprocs=16;
max_s=10;
tol=0.0;
cov=1;
rn=69.627;
zn=0.259;
rk=4.881;
zk=0.691;
a=0.736;

rm $cfname

python run_mcmc.py $cfname $indir $datdir $ofname $nprocs $max_s $tol $cov $rn $zn $rk $zk $a
bash $cfname

# Add information about run
info_file='mcmc_info.txt';
rm $info_file
INFO="run_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file