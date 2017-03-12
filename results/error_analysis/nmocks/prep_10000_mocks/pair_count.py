'''
For each of our mocks, perform pair counting and save a file.
'''
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    # get command filename, out_dir
    elements_needed = int(6)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    cfname    = args_array[1]
    mocks_dir = args_array[2]
    data_dir  = args_array[3]
    bins_dir  = args_array[4]
    Nmocks    = int(args_array[5])

    # get directories of scripts, executables, and star files
    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    pairs_dir   = scripts_dir + 'pair_count/'
    exe_dir     = './bin/'

    # Check for dir/file existence
    if not os.path.isdir(exe_dir):
        sys.stderr.write('{} does not exist Making directory...\n'.format(exe_dir))
        cmd = 'mkdir ' + exe_dir
        os.system(cmd)

    if not os.path.isdir(data_dir):
        sys.stderr.write('{} does not exist Making directory...\n'.format(data_dir))
        cmd = 'mkdir ' + data_dir
        os.system(cmd)

    pairs_file = exe_dir + 'pair_count'

    if not os.path.isfile(pairs_file):
        sys.stderr.write('{} does not exist. Compiling...\n'.format(pairs_file))
        # find system and use either icc or gcc
        current_sys = mwu.get_path.get_system()
        if current_sys=='bender':
            cmd = 'bash ' + pairs_dir + 'icc_compile_pair_count.sh ' + pairs_dir
        elif current_sys=='Adams-MacBook-Pro-2':
            cmd = 'bash ' + pairs_dir + 'gcc_compile_pair_count.sh ' + pairs_dir
        else:
            raise ValueError('Unrecognized system...\n')
        os.system(cmd)
    else:
        sys.stderr.write('Using already compiled file {}'.format(pairs_file))

    # Load todo list
    input_filename = cleaned_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Load bins file
    bins_file = bins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')
        sys.exit(1)

    # Write command file
    with open(cfname, 'w') as f:
        for i in range(Nmocks):

            out_dir = data_dir + 'sample_' + str(i) + '/'
            if not os.path.isdir(out_dir):
                cmd = 'mkdir ' + out_dir
                f.write(cmd)
                f.write('\n')

            samp_dir = mocks_dir + 'sample_' + str(i) + '/'

            for p in todo_list:

                in_file = samp_dir + 'mock_' + p.ID + '.xyzw.dat'

                if not os.path.isfile(in_file):
                    sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
                    continue

                output_file = out_dir + 'dd_' + p.ID + '.dat'

                cmd = pairs_file + ' ' + in_file + ' ' + bins_file + ' > ' + output_file
                f.write(cmd)
                f.write('\n')

if __name__ == '__main__':
    main()