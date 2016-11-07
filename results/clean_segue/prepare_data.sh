#!/usr/bin/bash

rm ../../data_segue_gdwarfs_cln/*.dat

python pickle_gstar_sample.py
python pointing_list.py
python separate_sample.py
python pointing_selection.py

# Add information about run
info_file='run_info.txt';
rm $info_file
INFO="prepare_data.sh was most recently run on:";
echo $INFO > $info_file
date >> $info_file

echo Time of run output to $info_file