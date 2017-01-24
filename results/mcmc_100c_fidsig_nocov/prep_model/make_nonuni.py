'''
A sample script to create a single mock. Here, we use our default parameters
but we could pass others. This script outputs a file containing executable
commands used in the mock creation. This script is called by a bash script
"test_mock.sh" where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    # get command filename, out_dir, nprocs, nmocks
    elements_needed = int(9)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname  = args_array[1]
    out_dir = args_array[2]
    sf = args_array[3]
    rn = args_array[4]
    zn = args_array[5]
    rk = args_array[6]
    zk = args_array[7]
    a  = args_array[8]


    # get directories of scripts and executables
    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mock_dir = scripts_dir + 'prepare_points/prepare_nonuniform/'
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

    cmd1 = (
        exe_file + ' -l_td ' + str(len(todo_dir)) + ' -td ' + todo_dir
        + ' -l_od ' + str(len(out_dir)) + ' -od ' + out_dir + ' -sf ' + sf
        + ' -rn ' + rn + ' -zn ' + zn + ' -rk ' + rk + ' -zk ' + zk + ' -a ' + a
        )
    cmd2 = 'python ' + mock_dir + '/clean_mocks.py ' + todo_dir + ' ' + out_dir + ' ' + sf
    cmd3 = 'rm ' + out_dir + 'temp*'
    cmd4 = 'python ' + mock_dir + '/xyzw_to_ZRW.py ' + todo_dir + ' ' + out_dir

    # Write commands to file
    with open(cfname, 'w') as f:
        f.write(cmd1)
        f.write('\n')
        f.write(cmd2)
        f.write('\n')
        f.write(cmd3)
        f.write('\n')
        f.write(cmd4)
        f.write('\n')

if __name__ == '__main__':
    main()
