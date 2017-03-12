#!/usr/bin/bash

if [[ $# -ne 1 ]] ; then
    echo "usage: ./pair_count_openmp num_threads"
    exit 1
fi

cfname='pairs_cmd_omp.txt';
out_dir='./pairs_data_omp/'

rm $cfname
rm -rf $out_dir
mkdir $out_dir

export OMP_NUM_THREADS=$1

python make_bins.py $out_dir
python pair_count_omp.py $cfname $out_dir
bash $cfname

# Add information about run
info_file='pairs_omp_info.txt';
rm $info_file
INFO="test_omp.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file