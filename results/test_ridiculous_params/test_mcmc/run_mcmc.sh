#!/usr/bin/bash

cfname='mcmc_cmd.txt';
indir='/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_fidcov_nonuni/data/';
datdir='./data/';
ofname='results.dat';
nprocs=16;
max_s=30000;
tol=0.0;
cov=1;
# rn=69.627;
# zn=0.259;
# rk=4.881;
# zk=0.691;
# a=0.736;
zk=0.675;
rk=2.397;
zn=0.234;
rn=2.027;
a=0.053;
# zk=0.620759;
# rk=3.576686;
# zn=0.201391;
# rn=7.220003;
# a=0.282755;



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