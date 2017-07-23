'''
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, nprocs, nmocks, params
    elements_needed = int(4)
    args_array = np.array(sys.argv)
    N_args     = len(args_array)
    assert(N_args == elements_needed)
    Njk      = args_array[1]
    uni_dir = args_array[2]
    out_dir  = args_array[3]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file = scripts_dir + '/errors/prepare_jk_uniform.py'

    # Check for dir existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(uni_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(uni_dir))
        sys.exit()

    # create commands to be executed
    cmd = (
        'python ' + exe_file + ' ' + Njk + ' ' + todo_dir + ' ' + uni_dir
        + ' ' + out_dir
        )
    os.system(cmd)

if __name__ == '__main__':
    main()
