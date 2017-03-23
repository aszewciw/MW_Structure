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
    elements_needed = int(7)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    out_dir   = args_array[1]
    data_dir  = args_array[2]
    model_dir = args_array[3]
    stats_dir = args_array[4]
    fid_dir   = args_array[5]
    bins_dir  = args_array[6]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mcmc_dir = scripts_dir + 'mcmc/mcmc_prep/'
    exe_file = mcmc_dir + 'prepare_files.py'

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making.\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    # create commands to be executed
    cmd =   (
            'python ' + exe_file + ' ' + out_dir + ' ' + todo_dir + ' '
            + data_dir + ' ' + model_dir + ' ' + stats_dir + ' ' + fid_dir
            + ' ' + bins_dir
            )

    os.system(cmd)

if __name__ == '__main__':
    main()
