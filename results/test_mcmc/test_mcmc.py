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
    elements_needed = int(6)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname = args_array[1]
    in_dir = args_array[2]
    ofname = args_array[3]
    nprocs = args_array[4]
    nsteps = args_array[5]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mcmc_dir = scripts_dir + 'mcmc/mcmc_mpi/'
    exe_file = mcmc_dir + 'bin/run_mcmc'

    # Check for dir/file existence
    if not os.path.isdir(in_dir):
        sys.stderr.write('{} does not exist. Please make dir and fill with data.\n'.format(in_dir))
        sys.exit()

    if not os.path.isfile(exe_file):
        sys.stderr.write('{} does not exist. Making...\n'.format(exe_file))
        cmd = 'make -C ' + mcmc_dir
        os.system(cmd)

    # create commands to be executed
    cmd = (
        'time mpirun -n ' + nprocs + ' ' + exe_file + ' -fn ' + ofname
        + ' -l_id ' + str(len(in_dir)) + ' -id ' + in_dir + ' -N_s ' + nsteps
        + ' -cov 1'
        )

    # Write commands to file
    with open(cfname, 'w') as f:
        f.write(cmd)
        f.write('\n')

if __name__ == '__main__':
    main()
