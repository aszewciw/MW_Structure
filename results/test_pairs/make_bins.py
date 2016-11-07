import mw_utilities_python as mwu
# import sys, pickle, math, os, string
#------------------------------------------------------------------------------#
'''
Make a set of distance bins, and output in different format.
These will be used for error calculation and mcmc.
'''
#------------------------------------------------------------------------------#

def main():

    # Make default radial bins
    data_dir = './data/'
    mwu.corr_prep.set_rbins(filepath=data_dir)


if __name__ == '__main__':
    main()

