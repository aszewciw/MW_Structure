#!/usr/bin/bash

cfname=prep_cmd.txt;
out_dir=./data/;
data_dir=../prep_data_samps/data/;
model_dir=../prep_model_nonuniform/data/;
dd_jk_dir=../prep_jk_frac_errors/data/data_mocks/;
rr_jk_dir=../prep_jk_frac_errors/data/data_uniform/;
bins_dir=../prep_bins/;
Ndata=100;

rm $cfname

python prepare_mcmc.py $cfname $out_dir $data_dir $model_dir $dd_jk_dir \
$rr_jk_dir $bins_dir $Ndata
bash $cfname

# Add information about run
info_file=prep_info.txt;
rm $info_file
INFO="prepare_mcmc.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file