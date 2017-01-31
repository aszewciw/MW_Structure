'''
For each of our 1000 mocks, perform pair counting and save a file.
'''
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    # get command filename, out_dir
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname    = args_array[1]
    pairs_dir = args_array[2]
    out_dir   = args_array[3]
    Nmocks    = args_array[4]

    # get directories of scripts, executables, and star files
    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file    = scripts_dir + 'errors/real_errors.py'

    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    # Write command file
    with open(cfname, 'w') as f:
        cmd = ( 'python ' + exe_file + ' ' + cleaned_dir + ' ' + pairs_dir + ' '
            + out_dir + ' ' + Nmocks )
        f.write(cmd)
        f.write('\n')

if __name__ == '__main__':
    main()