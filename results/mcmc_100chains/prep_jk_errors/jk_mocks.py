'''
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, nprocs, nmocks, params
    elements_needed = int(5)
    args_array = np.array(sys.argv)
    N_args     = len(args_array)
    assert(N_args == elements_needed)
    Nsamp    = int(args_array[1])
    Njk      = args_array[2]
    mock_dir = args_array[3]
    out_dir  = args_array[4]

    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file = scripts_dir + '/errors/prepare_jk_mock.py'

    # Check for dir existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(mock_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(mock_dir))
        sys.exit()

    for i in range(Nsamp):

        sys.stderr.write('On sample {} of {}\n'.format(i, Nsamp))

        samp_dir = mock_dir + 'sample_' + str(i) + '/'
        jk_dir = out_dir + 'sample_' + str(i) + '/'

        # Check for dir existence
        if not os.path.isdir(jk_dir):
            sys.stderr.write('{} does not exist. Making directory...\n'.format(jk_dir))
            cmd = 'mkdir ' + jk_dir
            os.system(cmd)

        if not os.path.isdir(samp_dir):
            sys.stderr.write('{} does not exist. Exiting...\n'.format(samp_dir))
            sys.exit()

        # create commands to be executed
        cmd = (
            'python ' + exe_file + ' ' + Njk + ' ' + todo_dir + ' ' + samp_dir
            + ' ' + jk_dir
            )
        os.system(cmd)

if __name__ == '__main__':
    main()
