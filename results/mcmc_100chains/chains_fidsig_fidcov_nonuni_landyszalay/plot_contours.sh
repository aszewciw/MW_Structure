#!/usr/bin/bash

cut_frac=0.05;
rn=2.027;
zn=0.234;
rk=2.397;
zk=0.675;
a=0.053;

lastfile=13;

plots_dir=./contours;
rm -rf $plots_dir;
mkdir $plots_dir;

for i in $(seq 0 $lastfile);
do
    data=./out_data/results_$i.dat;
    pltname=$plots_dir/contours_$i.png;
    python plot_contours.py $data $pltname $cut_frac $zn $rn $zk $rk $a
done
