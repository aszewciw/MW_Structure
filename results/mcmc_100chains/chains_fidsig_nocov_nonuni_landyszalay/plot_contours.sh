#!/usr/bin/bash

data1=/fs1/szewciw/MW_Structure/results/mcmc_100chains/chains_fidsig_nocov_nonuni/out_data/results_0.dat;
pltname1=contours_fidsig_nocov_nonuni.png

data2=./out_data/results.dat;
pltname2=contours_fidsig_nocov_nonuni_exclbin0.png;

cut_frac=0.05;
rn=2.027;
zn=0.234;
rk=2.397;
zk=0.675;
a=0.053;

Nfiles=13;

# python plot_contours.py $data1 $pltname1 $cut_frac $zn $rn $zk $rk $a
# python plot_contours.py $data2 $pltname2 $cut_frac $zn $rn $zk $rk $a

for i in $(seq 0 $Nfiles);
do
    echo $i;
done
