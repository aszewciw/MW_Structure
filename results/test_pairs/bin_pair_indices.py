'''
Produce file containing pair counts for SEGUE data.
'''

import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    pairs_dir   = scripts_dir + 'pair_count/'
    out_dir     = './data/'

    pairs_file = './bin_pair_indices'
    if not os.path.isfile(pairs_file):
        sys.stderr.write('{} does not exist. Compiling...\n'.format(pairs_file))
        # find system and use either icc or gcc
        current_sys = mwu.get_path.get_system()
        if current_sys=='bender':
            cmd = 'bash ' + pairs_dir + 'icc_compile_bin_pair_indices.sh ' + pairs_dir
        elif current_sys=='Adams-MacBook-Pro-2':
            cmd = 'bash ' + pairs_dir + 'gcc_compile_bin_pair_indices.sh ' + pairs_dir
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

    bins = np.genfromtxt(bins_file, skip_header=1)
    n_bins = len(bins)

    for p in todo_list:

        in_file = cleaned_dir + 'star_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        cmd = './bin_pair_indices ' + in_file + ' ' + bins_file
        os.system(cmd)

        for i in range(n_bins):

            pair_file = './pairs_bin_' + str(i) + '.dat'

            cmd = ('mv ' + pair_file + ' ' + out_dir + 'pair_indices_p' + p.ID
                    + '_b' + str(i) + '.dat' )
            os.system(cmd)


if __name__ == '__main__':
    main()