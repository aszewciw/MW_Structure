'''
A sample script to create a number of mocks. Here, we use our default parameters
but we could pass others. This file reads in the number of mocks we wish to
create and the number of processes we wish to use. It outputs a file containing
executable commands used in the mock creations. This script is called by a bash
script "test_mocks.sh" where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, nprocs, nmocks
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname  = args_array[1]
    out_dir = args_array[2]
    nprocs  = args_array[3]
    nmocks  = args_array[4]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mock_dir = scripts_dir + 'prepare_points/prepare_mocks/'
    exe_file = mock_dir + 'bin/make_galaxy'

    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isfile(exe_file):
        sys.stderr.write('{} does not exist. Making...'.format(exe_file))
        cmd = 'make -C ' + mock_dir
        os.system(cmd)

    # create commands to be executed
    cmd1 = (
        'time mpirun -n ' + nprocs + ' ' + exe_file + ' -N_m ' + nmocks
        + ' -l_td ' + str(len(todo_dir)) + ' -td ' + todo_dir
        + ' -l_od ' + str(len(out_dir)) + ' -od ' + out_dir
        )
    cmd2 = (
        'python ' + mock_dir + '/clean_mocks.py ' + todo_dir + ' '
        + out_dir + ' ' + nmocks
        )
    cmd3 = 'rm ' + out_dir + 'temp*'

    # Write commands to file
    with open(cfname, 'w') as f:
        f.write(cmd1)
        f.write('\n')
        f.write(cmd2)
        f.write('\n')
        f.write(cmd3)
        f.write('\n')

if __name__ == '__main__':
    main()
