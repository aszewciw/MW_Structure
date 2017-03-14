'''
We're going to plot how sigma changes as we increase the number of mocks used to
generate sigma.
In particular
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

def main():

    # get command filename, out_dir
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    if N_args < 7:
        sys.stderr.write("Not enough arguments were passed.\n")
        sys.exit()
    pairs_dir = args_array[1]
    out_dir   = args_array[2]
    bins_dir  = args_array[3]
    nsubsets  = int(args_array[4])
    nmocks_array = []
    for i in range(nsubsets):
        nmocks_array.append(args_array[5+i])

    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(pairs_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(pairs_dir))
        sys.exit()

    # Load list of pointing IDs
    todo_dir = mwu.get_path.get_cleandata_path()
    todo_file = todo_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins file
    bins_file = bins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')
        sys.exit(1)
    bins_mid = np.genfromtxt(bins_file, unpack=True, usecols=[2], skip_header=1)
    Nbins = len(bins_mid)

    std_dict={}
    for n in nmocks_array:
        std_dict[n]=np.zeros((Nbins, Nbins))

    # Load all data into dictionary
    for n in nmocks_array:
        data_dir = out_dir + n
        for i in range(N_los):
            std_file = data_dir + '/mean_std_' + ID[i] + '.dat'
            if not os.path.isfile(std_file):
                sys.stderr.write('Error: {} does not exist\n'.format(std_file))
                sys.exit()
            std = np.genfromtxt(std_file, unpack=True, usecols=[1])
            std_dict[n][i,:] = std

    # We'll compare standard deviations to the one from the largest nmocks
    std_true = std_dict[nmocks_array[-1]]

    std_means = {}

    # average of absolute value of fractional deviations
    for n in nmocks_array:
        std_dict[n] = np.fabs(std_dict[n] - std_true) / std_true
        std_means[n] = np.mean(std_dict[n], axis=0)

    plt.clf()
    plt.figure(1)
    for n in nmocks_array:
        plt.semilogx(bins_mid, std_means[n], label=n)

    plt.legend(loc='upper right')
    plt.xlabel('bin centers (kpc)')
    plt.ylabel('fractional sigma difference')
    plt.savefig(out_dir + '/sigma_diff.png')


if __name__ == '__main__':
    main()