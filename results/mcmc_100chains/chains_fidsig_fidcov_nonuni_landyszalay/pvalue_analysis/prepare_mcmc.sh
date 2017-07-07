#!/usr/bin/bash

cfname=prep_cmd.txt;
out_dir=./data/;
data_dir=../prep_dddr/data/;
model_dir=../../prep_model_nonuniform/data/;
mr_dir=../prep_mr/data/;
stats_dir=../prep_corrmatrixDATAPARAMS/errors_data/;
fid_dir=../prep_corrmatrixDATAPARAMS/errors_data/;
bins_dir=../../prep_bins/;
Ndata=100;

rm $cfname

python prepare_mcmc.py $cfname $out_dir $data_dir $model_dir $mr_dir $stats_dir $fid_dir $bins_dir $Ndata
bash $cfname

# Add information about run
info_file=prep_info.txt;
rm $info_file
INFO="prepare_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file