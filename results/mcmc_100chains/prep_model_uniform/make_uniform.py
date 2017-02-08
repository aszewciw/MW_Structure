'''
A sample script to create a uniform points. Here, we use our default parameters
but we could pass others. This file reads in the ratio of N_uniform/N_data for
all SEGUE pointings. It outputs a file containing executable commands used in
the uniform sample creations. This script is called by a bash script
"test_uniform.sh" where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, num_ratio
    elements_needed = int(4)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname    = args_array[1]
    out_dir   = args_array[2]
    num_ratio = args_array[3]

    # get directories of scripts and executables
    todo_dir    = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    uniform_dir = scripts_dir + 'prepare_points/uniform/'

    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    # create commands to be executed
    cmd = ( 'python ' + uniform_dir + 'generate_uniform.py ' + num_ratio + ' '
        + todo_dir + ' ' + out_dir )

    # Write commands to file
    with open(cfname, 'w') as f:
        f.write(cmd)

if __name__ == '__main__':
    main()