import mw_utilities_python as mwu
import sys, pickle, math, os, string, random
import numpy as np

def main():

    # Parse CL
    elements_needed = int(6)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    N_jackknife = int(args_array[1])
    todo_dir    = args_array[2]
    bins_dir    = args_array[3]
    jk_dir      = args_array[4]
    out_dir     = args_array[5]

    if not(os.path.isdir(out_dir)):
        sys.stderr.write('{} does not exist. Making...\n'.format(out_dir))
        cmd='mkdir ' + out_dir
        os.system(cmd)

    # load the todo pointing list
    input_filename = todo_dir + 'todo_list.dat'
    if not(os.path.isfile(input_filename)):
        sys.write('Error: {} does not exist. Exiting...\n'.format(input_filename))
        sys.exit()
    sys.stderr.write('Loading pointing info from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list  = pickle.load(input_file)
    input_file.close()

    # load bin settings
    bins_filename = bins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_filename):
        sys.stderr.write('Error: {} does not exist. Exiting...\n'.format(bins_filename))
        sys.exit()

    bins = np.genfromtxt(bins_filename, skip_header=1)
    N_rbins = len(bins)

    cleaned_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    pairs_dir   = scripts_dir + 'pair_count/'
    exe_dir     = './bin/'

    # Check for dir/file existence
    if not os.path.isdir(exe_dir):
        sys.stderr.write('{} does not exist Making directory...'.format(exe_dir))
        cmd = 'mkdir ' + exe_dir
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



    # Main loop
    for p in todo_list:

        # counting pairs for the whole sample
        data_filename = data_dir + 'mock_' + p.ID + '.xyzw.dat'
        counts_filename = data_dir + 'mock_' + p.ID + '_jk_all.ddcounts.dat'
        cmd = (pairs_file + ' ' + data_filename + ' ' + bins_filename
               + ' > ' + counts_filename)
        os.system(cmd)

        # load dd counts, weighted and normalized
        counts_all = np.genfromtxt(counts_filename, unpack=True, usecols=[4])

        # Make array to store dd counts for different jackknife samples
        counts_jk = np.zeros((N_jackknife, N_rbins))

        # counting pairs for each jackknife sample and load pairs into array
        for i in range(N_jackknife):
            jackknife_filename = data_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.dat'
            counts_filename = data_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.ddcounts.dat'
            cmd = (pairs_file + ' ' + jackknife_filename + ' ' + bins_filename
                   + ' > ' + counts_filename)
            os.system(cmd)
            counts_jk[i,:] = np.genfromtxt(counts_filename, unpack=True, usecols=[4])


        jk_std  = np.std(counts_jk, axis=0) * np.sqrt(N_jackknife-1)

        output_filename = data_dir + 'mock_' + p.ID + '_jk_error.dat'
        np.savetxt(output_filename, jk_std, fmt='%1.6f')


if __name__ == '__main__':
    main()

