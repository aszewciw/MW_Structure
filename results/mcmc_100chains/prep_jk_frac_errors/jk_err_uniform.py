'''
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():
    # Parse CL
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    N_jk     = args_array[1]
    bins_dir = args_array[2]
    jk_dir   = args_array[3]
    out_dir  = args_array[4]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file = scripts_dir + '/errors/jk_error_uniform.py'

    # Check for dir existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(jk_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(jk_dir))
        sys.exit()

    # create commands to be executed
    cmd = (
        'python ' + exe_file + ' ' + N_jk + ' ' + todo_dir + ' ' + bins_dir
        + ' ' + jk_dir + ' ' + out_dir
        )
    os.system(cmd)

if __name__ == '__main__':
    main()
