# Cleaning of SEGUE data

## Files run in the following order:
* __pickle_gstar_sample.py__ - select only gdwarfs from raw data
* __pointing_list.py__ - output coordinate info on SEGUE plates
* __separate_sample.py__ - assign gdwarfs to pointings and output file for each pointing
* __pointing_selection.py__ - select pointings in which we have enough stars within 1-3 kpc; output xyzw file for each pointing