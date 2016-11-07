# MW_Structure

## Probing the structure of the Milky Way by employing the two point correlation function on SEGUE g-dwarfs

## Notes on folder names:
* __scripts__ - various pieces of code used in analysis (e.g. pair counting, mcmc, jackknife, etc.)
* __results__ - essentially a history of the different runs performed
    * (a) python and bash scripts which call other scripts in "scripts" folder
        * generally speaking, these python and bash scripts will pass different input to the source code in scripts
    * (b) intermediate (e.g. mock files, uniform files, error files, etc.) and final output (e.g. mcmc results)
    * (c) a date and time log of when the script was run
* __data_segue_raw__ - raw, unprocessed SEGUE data
* __data_segue_gdwarfs_cln__ - cleaning of SEGUE using selection criteria from ./scripts/clean_segue_data/ and described in Mao et al. 2015
    * Because this data is really only cleaned once I chose not to place it in ./results/
    * Also, files present in this folder are used repeatedly to decide such things as how many mock and uniform stars populate a particular l.o.s.
* _other?_ - as of now, no other selections were made using the SEGUE data. Perhaps some other selections will be made in the future

## Please see the .ipynb (not yet produced) for a more detailed description of the project.

## All scripts currently use the latest conda installation of packages in Python3 and have not been confirmed to be compatible with Python2