'''
calcualte errors in dd for jk on a mock

Note: I find rounding errors when I don't use raw pair counts. Idk why, but I'm
going to find the jk stdev using raw pair counts and then just do the normalization.
'''
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
        sys.stderr.write('{} does not exist Making directory...\n'.format(exe_dir))
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

        # Make array to store raw dd counts for different jackknife samples
        counts_jk = np.zeros((N_jackknife, N_rbins))
        # Each file will have the exact same norm b/c same N
        norm = np.zeros(N_rbins)

        # counting pairs for each jackknife sample and load pairs into array
        for i in range(N_jackknife):
            jackknife_filename = jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            counts_filename = jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.rrcounts.dat'
            cmd = (pairs_file + ' ' + jackknife_filename + ' ' + bins_filename
                   + ' > ' + counts_filename)
            os.system(cmd)
            counts_jk[i,:], norm = np.genfromtxt(counts_filename, unpack=True, usecols=[5, 6])

        jk_mean = np.mean(counts_jk, axis=0)
        jk_std  = np.std(counts_jk, axis=0) * np.sqrt(N_jackknife-1)

        # Normalize counts
        jk_mean /= norm
        jk_std  /= norm
        jk_data = np.column_stack((jk_mean,jk_std))

        tol = 1e-8
        jk_frac = np.zeros(len(jk_mean))
        for i in range(len(jk_frac)):
            if(jk_mean[i]>tol):
                jk_frac[i] = jk_std[i] / jk_mean[i]

        output_filename = jk_dir + 'mean_std_' + p.ID + '.dat'
        np.savetxt(output_filename, jk_data, fmt='%1.6e')
        frac_filename = jk_dir + 'frac_err_jk_RR_' + p.ID + '.dat'
        np.savetxt(frac_filename, jk_frac, fmt='%1.6e')


if __name__ == '__main__':
    main()

