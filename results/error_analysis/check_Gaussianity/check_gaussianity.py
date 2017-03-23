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

def GIF_MOVIE(files, output_gif, delay=60, repeat=True, removef=False):
    """
    Given a list if 'files', it creates a gif file, and deletes temp files.

    Parameters
    ----------
    files: array_like
            List of abs. paths to temporary figures

    output_gif: str
            Absolute path to output gif file.
    """
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s' %( delay,loop," ".join(files), \
        output_gif) )

    if removef:
        for fname in files: os.remove(fname)


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

    png_list=[]

    for i in range(N_los):

        ID = ID_list[i]
        sys.stderr.write('On pointing {}\n'.format(ID))

        if ID!='27' and ID!='30':
            continue

        for j in range(N_mocks):

            dd_fname = pairs_dir + 'sample_' + str(j) + '/dd_' + ID + '.dat'
            DD_raw_all[j,:] = np.genfromtxt(dd_fname, unpack=True, comments='#',
                usecols=[5])

        sys.stderr.write('Data loaded. Making plots.\n')

        plt.clf()
        fig1=plt.figure(1)
        fig1.suptitle('Pair Histograms from 10000 mocks, l.o.s. ' + ID)
        bwidth=1

        for j in range(N_bins):
            label=str(np.round(bins_mid[j],3)) + ' kpc'
            fig1.add_subplot(4,3,j+1)
            fig1.set_xticklabels(fontsize='small')
            fig1.set_yticklabels(fontsize='small')
            DD = DD_raw_all[:,j]
            hist_bins = make_hist_bins(DD, bwidth)
            n, b, patches = plt.hist(DD, bins=hist_bins, facecolor='green',
                alpha=0.7, label=label)
            plt.legend(loc='upper right', fontsize=6)

        figname=out_dir + 'pair_hist_' + ID + '.png'
        plt.savefig(figname)

        png_list.append(figname)

        sys.stderr.write('Plots finished.\n')

    gif_name= out_dir + 'pair_hist.gif'
    GIF_MOVIE(png_list, gif_name, delay=120)


if __name__ == '__main__':
    main()