'''
For each of our 1000 mocks, perform pair counting and save a file.
'''
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    # get command filename, out_dir
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    if N_args < 6:
        sys.stderr.write("Not enough arguments were passed.\n")
        sys.exit()
    cfname    = args_array[1]
    pairs_dir = args_array[2]
    out_dir   = args_array[3]
    nsubsets  = int(args_array[4])
    nmocks_array = []
    for i in range(nsubsets):
        nmocks_array.append(args_array[4+i])

    # get directories of scripts, executables, and star files
    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file    = scripts_dir + 'errors/real_errors.py'

    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(pairs_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(pairs_dir))
        sys.exit()

    # Write command file
    with open(cfname, 'w') as f:
        for n in nmocks_array:
            tmp_dir = out_dir + n + '/'
            if not os.path.isdir(tmp_dir):
                sys.stderr.write('{} does not exist. Making directory...\n'
                    .format(tmp_dir))
                cmd = 'mkdir ' + tmp_dir
                os.system(cmd)

            cmd = ( 'python ' + exe_file + ' ' + cleaned_dir + ' ' + pairs_dir
                + ' ' + tmp_dir + ' ' + n )
            f.write(cmd)
            f.write('\n')

if __name__ == '__main__':
    main()