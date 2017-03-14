#!/usr/bin/bash

cfname=errors_cmd.txt;
pairs_dir=../data_pairs/;
out_dir=../data_errors;
nmocks='100 200 500 1000 2000 5000 10000';
arraylen=7;

rm $cfname

python calc_errors.py $cfname $pairs_dir $out_dir $arraylen $nmocks
bash $cfname

# Add information about run
info_file=errors_info.txt;
rm $info_file
INFO="calc_errors.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file