import pandas as pd
from scipy import linalg
import numpy as np
import sys, os

#------------------------------------------------------------------------------#
'''
For each SEGUE l.o.s., load the raw pair counts from 1000 mocks in each of 12
radial bins.

Calculate the covariance matrix. Output a file.
'''
#------------------------------------------------------------------------------#

def main():

    # Parse CL
    elements_needed = int(5)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    todo_dir  = args_array[1]
    pairs_dir = args_array[2]
    out_dir   = args_array[3]
    Nmocks    = int(args_array[4])

    # Load list of pointing IDs
    todo_file = todo_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Get number of bins by loading one pair counts file
    counts_file = pairs_dir + 'sample_0/dd_0.dat'
    dd = np.genfromtxt( counts_file, dtype=float, unpack=True, usecols=[4] )
    N_bins = len(dd)

    # Create a file containing all normed counts
    for ID in ID_list:

        dd_all = np.zeros((Nmocks, N_bins))

        # loop over all mocks
        for i in range(N_mocks):

            # Load counts for a single mock
            counts_file = pairs_dir + 'sample_' + str(i) + '/dd_' + ID + '.dat'
            dd_all[i] = np.genfromtxt( counts_file, dtype=float, unpack=True, usecols=[4] )

        # Output data
        output_filename = out_dir + 'normed_counts_all_' + p.ID + '.dat'
        np.savetxt(output_filename, dd_all, fmt='%.6e')

        sys.stderr.write('Calculating covariance for pointing {}\n'.format(ID))

        # Load normalized counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = mocks_1000_dir + 'normed_counts_all_' + ID + '.dat'
        DD = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Calculate correlation matrix
        corr = DD.corr().values

        out_file = out_dir + 'correlation_' + ID + '.dat'
        np.savetxt(out_file, corr, fmt='%.6f')

        # Invert covariance matrix and save to file
        inv_corr = linalg.inv(corr)

        out_file = out_dir + 'inv_correlation_' + ID + '.dat'
        np.savetxt(out_file, inv_corr, fmt='%.6f')

if __name__ == '__main__':
    main()