import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():

    # get command filename, out_dir, nprocs, nmocks
    fname = 'mcmc_result_nocov_newsigs.dat'
    mcmc = pd.read_csv(fname, sep='\s+')

    Ntotal = len(mcmc)

    plt.clf()
    plt.figure(1)
    plt.subplot(321)
    plt.plot(mcmc['step'], mcmc['r0_thin'], color='b', label=r'$r_{0,thin}$')
    plt.ylabel(r'$r_{0,thin}$')
    plt.subplot(322)
    plt.plot(mcmc['step'], mcmc['z0_thin'], color='r', label=r'$z_{0,thin}$')
    plt.ylabel(r'$z_{0,thin}$')
    plt.subplot(323)
    plt.plot(mcmc['step'], mcmc['r0_thick'], color='g', label=r'$r_{0,thick}$')
    plt.ylabel(r'$r_{0,thick}$')
    plt.subplot(324)
    plt.plot(mcmc['step'], mcmc['z0_thick'], color='k', label=r'$z_{0,thick}$')
    plt.ylabel(r'$z_{0,thick}$')
    plt.subplot(325)
    plt.plot(mcmc['step'], mcmc['ratio'], color='c', label=r'$\frac{n_{thick}}{n_{thin}}$')
    plt.ylabel(r'$\frac{n_{thick}}{n_{thin}}$')
    plt.tight_layout()
    # plt.axis([0, Ntotal, 0, 0.5])
    # plt.xlabel('Step Number')
    # plt.ylabel(r'$\frac{|\sigma_{plus} - \sigma_{minus}|}{\sigma_{plus}}$', fontsize=24)
    # plt.legend(loc=2)
    plt.savefig('chain.png')

if __name__ == '__main__':
    main()
