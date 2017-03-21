# from config import *
# import matplotlib.pyplot as plt
# import pylab
# from scipy.stats import norm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mw_utilities_python as mwu
import sys, pickle, os
import numpy as np

# ---------------------------------------------------------------------------- #
'''
Contains histograms of the pair count distributions, produced from 1000 mocks.

Overplotted above the histogram is a Gaussian curve taken from the mean and
standard deviation.
'''
# ---------------------------------------------------------------------------- #

def make_hist_bins(x, bwidth):

    bin_min=int(min(x))
    bin_max=int(max(x))+bwidth

    bins=np.arange(bin_min,bin_max,bwidth)

    return bins




def main():

    args_array = np.array(sys.argv)
    N_args = len(args_array)
    N_mocks = int(args_array[1])
    pairs_dir = args_array[2]
    out_dir = args_array[3]
    bins_dir = args_array[4]


    # Check for dir/file existence
    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...\n'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isdir(pairs_dir):
        sys.stderr.write('{} does not exist. Exiting...\n'.format(errors_dir))
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
    N_bins = len(bins_mid)

    DD_raw_all = np.zeros((N_mocks, N_bins))

    for i in range(N_los):
        ID = ID_list[i]
        if ID != '27':
            continue
        sys.stderr.write('On pointing {}\n'.format(ID))

        for j in range(N_mocks):

            dd_fname = pairs_dir + 'sample_' + str(j) + '/dd_' + ID + '.dat'
            DD_raw_all[j,:] = np.genfromtxt(dd_fname, unpack=True, comments='#',
                usecols=[5])

        sys.stderr.write('Data loaded. Making plots.\n')

        plt.clf()
        plt.figure(1)
        spnum = 431
        bwidth=1

        for j in range(N_bins):
            label=str(np.round(bins_mid,3)) + ' kpc'
            plt.subplot(spnum+j)
            DD = DD_raw_all[:,j]
            hist_bins = make_hist_bins(DD, bwidth)
            n, b, patches = plt.hist(DD, bins=hist_bins, facecolor='green',
                alpha=0.7, label=label)
            plt.legend(loc='upper right', fontsize=6)

        figname=out_dir + 'pair_hist_' + ID + '.png'
        plt.savefig(figname)

        sys.stderr.write('Plots finished.\n')






    # # loop over each l.o.s.
    # for p in todo_list:

    #     if p.ID != '27':
    #         continue

    #     sys.stderr.write('Making histogram for pointing {}\n'.format(p.ID))

    #     # Empty arrays where each row is counts for 1 mock in current l.o.s.
    #     DD_raw_all = np.zeros((N_mocks, N_bins))
    #     DD_all     = np.zeros((N_mocks, N_bins))

    #     # loop over all mocks and add DD values to array
    #     for i in range(N_mocks):

    #         # Load counts for a single mock
    #         corr_file = ( data_dir + 'mock_' + str(i+1) + '/mock_pairs_'
    #             + p.ID + '.dat' )
    #         DD_raw_all[i], DD_all[i] = np.genfromtxt( corr_file, unpack=True,
    #             usecols=[4, 5] )

    #     # Load mean and standard deviation
    #     stats_file = stats_dir + 'stats_' + p.ID + '.dat'
    #     mu_list, sigma_list = np.genfromtxt(stats_file, unpack=True,
    #                             usecols=[0,2])

    #     # Plot histogram for each bin
    #     for i in range(N_bins):

    #         # get current array for hist
    #         DD = DD_all[:, i]

    #         # Make histogram bins
    #         hist_min  = min(DD)
    #         hist_max  = max(DD)
    #         offset    = 0.001*hist_max
    #         hist_max  += offset # make sure max is in a bin
    #         N_hist    = 30
    #         hist_bins = np.linspace(hist_min, hist_max, num=50)

    #         # Get normalized counts, bin edges, bin centers
    #         counts, edges = np.histogram(DD, hist_bins, normed=True)
    #         binWidth      = edges[1] - edges[0]
    #         centers       = edges[:-1]+0.5*(edges[1:]-edges[:-1])

    #         # Plot bar graph with transparency
    #         # Multiply by binWidth because np.histogram divides by it by default
    #         plt.clf()
    #         plt.figure(1)
    #         plt.bar(centers, counts*binWidth, binWidth, color='blue', alpha=0.1)

    #         # Add a normal curve on top of the histogram
    #         mu    = mu_list[i]
    #         sigma = sigma_list[i]
    #         x     = np.linspace(centers[0], centers[-1], N_hist)
    #         plt.plot(x, norm.pdf(x, mu, sigma)*binWidth, color='r')

    #         # Save figure
    #         figure_name = ( plots_dir + 'histogram_' + p.ID + 'bin_' + str(i)
    #                         + '.png' )
    #         plt.savefig(figure_name)


if __name__ == '__main__':
    main()