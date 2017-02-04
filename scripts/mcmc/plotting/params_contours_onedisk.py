#!/usr/bin/env python
'''
Create plots for an MCMC chain.

For a list of MCMC data files, create the following plots:
1. r0_thick vs r0_thin (contour)
2. z0_thick vs z0_thin (contour)
3. chi2 color-barred steps for each parameter

My MCMC files output the following columns:
    step number
    chi2
    reduced chi2
    r0_thin
    z0_thin
    r0_thick
    z0_thick
    thick_thin_ratio
'''

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import corner
import pandas as pd
import sys
import numpy as np


def main():

    # get command filename, out_dir, nprocs, nmocks
    elements_needed = int(6)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    in_fname  = args_array[1]
    plot_name = args_array[2]
    cut_frac  = float(args_array[3])
    z0_thin_true  = float(args_array[4])
    r0_thin_true  = float(args_array[5])

    # Load MCMC data frame
    MCMC = pd.read_csv(in_fname, sep='\s+')

    # Check that names were included in header
    if MCMC.columns[0]!='step':
        print('This file needs header names as its first row!')
        sys.exit(-1)

    # Cut a fraction of the data as "burn-in"
    N_drop = len(MCMC) * cut_frac
    MCMC   = MCMC[MCMC['step']>N_drop]

    # Set significance levels for contour plots
    signif_levels = np.array([1.0,2.0,3.0])
    levels = 1.0 - np.exp(-0.5*signif_levels**2)

    print('Beginning Plotting...')

    # Plot all 5 params on one graph
    x = np.column_stack((MCMC['z0_thin'].values, MCMC['r0_thin'].values))
    fig = corner.corner(x, levels=levels, labels=["$Z_{0,thin}$", "$R_{0,thin}$"],
        truths=[z0_thin_true, r0_thin_true])
    fig.suptitle("Mock MCMC Results")
    plt.savefig(plot_name)

if __name__ == '__main__':
    main()