'''
Produce file containing pair counts for SEGUE data.
'''

import mw_utilities_python as mwu
import sys, pickle, os

def main():

    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    pairs_dir   = scripts_dir + 'pair_count/'
    out_dir     = './data/'
    uni_dir = '../test_points/data/'
    exe_dir = './bin/'

    if not os.path.isdir(exe_dir):
        sys.stderr.write('{} does not exist Making directory...'.format(exe_dir))
        cmd = 'mkdir ' + exe_dir
        os.system(cmd)

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
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

    input_filename = cleaned_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    bins_file = out_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    for p in todo_list:

        in_file = cleaned_dir + 'star_' + p.ID + '.xyzw.dat'
        # in_file = uni_dir + 'uniform_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = out_dir + 'dd_' + p.ID + '.dat'

        cmd = pairs_file + ' ' + in_file + ' ' + bins_file + ' > ' + output_file
        os.system(cmd)

if __name__ == '__main__':
    main()