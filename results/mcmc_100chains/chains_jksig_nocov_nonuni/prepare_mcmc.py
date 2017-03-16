'''
A sample script to run an mcmc chain. We assume that all of the data has been
prepared in the "in_dir" folder. It outputs a file containing executable commands
used in the mock creations. This script is called by a bash script "test_mcmc.sh"
where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, nprocs, nmocks
    elements_needed = int(10)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname    = args_array[1]
    out_dir   = args_array[2]
    data_dir  = args_array[3]
    model_dir = args_array[4]
    stats_dir = args_array[5]
    fid_dir   = args_array[6]
    bins_dir  = args_array[7]
    Ndata     = args_array[8]
    cov       = args_array[9]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mcmc_dir = scripts_dir + 'mcmc/mcmc_prep/'
    exe_file = mcmc_dir + 'prepare_files_multi_data.py'

    # create commands to be executed
    cmd =   (
            'python ' + exe_file + ' ' + out_dir + ' ' + todo_dir + ' '
            + data_dir + ' ' + model_dir + ' ' + stats_dir + ' ' + fid_dir
            + ' ' + bins_dir + ' ' + Ndata + ' ' + cov
            )

    # Write commands to file
    with open(cfname, 'w') as f:
        f.write(cmd)
        f.write('\n')

if __name__ == '__main__':
    main()
