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
    elements_needed = int(8)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname   = args_array[1]
    in_dir   = args_array[2]
    data_dir = args_array[3]
    out_dir  = args_array[4]
    nprocs   = args_array[5]
    max_s    = args_array[6]
    tol      = args_array[7]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mcmc_dir = scripts_dir + 'mcmc/mcmc_mpi/'
    exe_file = mcmc_dir + 'bin/run_mcmc'

    # Check for dir/file existence
    if not os.path.isdir(in_dir):
        sys.stderr.write('{} does not exist. Please make dir and fill with data.\n'.format(in_dir))
        sys.exit()

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(data_dir):
        sys.stderr.write('{} does not exist. Please make dir and fill with data.\n'.format(data_dir))
        sys.exit()

    if not os.path.isfile(exe_file):
        sys.stderr.write('{} does not exist. Making...\n'.format(exe_file))
        cmd = 'make -C ' + mcmc_dir
        os.system(cmd)

    # Write commands to file
    with open(cfname, 'w') as f:

        ofname = out_dir + 'results.dat'

        cmd = (
            'time mpirun -n ' + nprocs + ' ' + exe_file + ' -fn ' + ofname
            + ' -l_id ' + str(len(in_dir)) + ' -id ' + in_dir + ' -max_s ' + max_s
            + ' -tol ' + tol + ' -dd ' + data_dir + ' -l_dd ' + str(len(data_dir))
            )
        f.write(cmd)
        f.write('\n')

if __name__ == '__main__':
    main()
