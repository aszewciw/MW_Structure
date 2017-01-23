#!/usr/bin/bash

cfname='prep_cmd.txt';
out_dir='./data/';
data_dir='./prep_data/data/';
model_dir='./prep_model/data/';
stats_dir='./prep_errors/errors_data/';
fid_dir='./prep_errors/errors_data/';

rm $cfname

python prepare_mcmc.py $cfname $out_dir $data_dir $model_dir $stats_dir $fid_dir
bash $cfname

# Add information about run
info_file='prep_info.txt';
rm $info_file
INFO="prepare_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file