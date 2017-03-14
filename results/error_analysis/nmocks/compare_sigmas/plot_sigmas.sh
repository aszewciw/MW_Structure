#!/usr/bin/bash

errors_dir=../../data_errors;
out_dir=./plots/;
bins_dir=../../prep_bins/;
nmocks='100 200 500 1000 2000 5000 10000';
arraylen=7;

python plot_sigmas.py $errors_dir $out_dir $bins_dir $arraylen $nmocks