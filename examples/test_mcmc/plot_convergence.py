import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():

    # get command filename, out_dir, nprocs, nmocks
    fname = 'mcmc_result_nocov.dat'
    mcmc = pd.read_csv(fname, sep='\s+')

    Ntotal = len(mcmc)
    Nsteps = 20000
    Nparams = 5

    # First, print the standard deviations I'm interested in
    frac_delete = 0.1
    ind_delete = int(frac_delete*Ntotal)
    std = np.std(mcmc['r0_thin'].values[ind_delete:])
    print('rthin std is ', std)
    std = np.std(mcmc['z0_thin'].values[ind_delete:])
    print('zthin std is ', std)
    std = np.std(mcmc['r0_thick'].values[ind_delete:])
    print('rthick std is ', std)
    std = np.std(mcmc['z0_thick'].values[ind_delete:])
    print('zthick std is ', std)
    std = np.std(mcmc['ratio'].values[ind_delete:])
    print('ratio std is ', std)


    Nseg = int(Ntotal/Nsteps)

    rthin_std  = np.zeros(Nseg)
    zthin_std  = np.zeros(Nseg)
    rthick_std = np.zeros(Nseg)
    zthick_std = np.zeros(Nseg)
    ratio_std  = np.zeros(Nseg)


    for i in range(Nseg):
        lower = i * Nsteps
        upper = lower + Nsteps
        rthin_std[i]  = np.std(mcmc['r0_thin'].values[lower:upper])
        zthin_std[i]  = np.std(mcmc['z0_thin'].values[lower:upper])
        rthick_std[i] = np.std(mcmc['r0_thick'].values[lower:upper])
        zthick_std[i] = np.std(mcmc['z0_thick'].values[lower:upper])
        ratio_std[i]  = np.std(mcmc['ratio'].values[lower:upper])

    step_num = np.arange(1, Nseg+1)*Nsteps

    plt.clf()
    plt.figure(1)
    plt.subplot(321)
    plt.plot(step_num, rthin_std)
    plt.ylabel(r'$\sigma_{r_{0,thin}}$ (kpc)')
    plt.subplot(322)
    plt.plot(step_num, zthin_std)
    plt.ylabel(r'$\sigma_{z_{0,thin}}$ (kpc)')
    plt.subplot(323)
    plt.plot(step_num, rthick_std)
    plt.ylabel(r'$\sigma_{r_{0,thick}}$ (kpc)')
    plt.subplot(324)
    plt.plot(step_num, zthick_std)
    plt.ylabel(r'$\sigma_{z_{0,thick}}$ (kpc)')
    plt.subplot(325)
    plt.plot(step_num, ratio_std)
    plt.ylabel(r'$\sigma_{ratio}$')
    plt.tight_layout()
    plt.savefig('stdev_' + str(Nsteps) + '.png')

    # Fractional differences in standard deviation
    rthin_f  = np.zeros(Nseg-1)
    zthin_f  = np.zeros(Nseg-1)
    rthick_f = np.zeros(Nseg-1)
    zthick_f = np.zeros(Nseg-1)
    ratio_f  = np.zeros(Nseg-1)

    # Compute fractional differences
    for i in range(Nseg):
        if i==0: continue

        rthin_f[i-1] = np.abs((rthin_std[i] - rthin_std[i-1])/rthin_std[i])
        zthin_f[i-1] = np.abs((zthin_std[i] - zthin_std[i-1])/zthin_std[i])
        rthick_f[i-1] = np.abs((rthick_std[i] - rthick_std[i-1])/rthick_std[i])
        zthick_f[i-1] = np.abs((zthick_std[i] - zthick_std[i-1])/zthick_std[i])
        ratio_f[i-1] = np.abs((ratio_std[i] - ratio_std[i-1])/ratio_std[i])

    frac_num = np.arange(1, Nseg)*Nsteps

    plt.clf()
    plt.figure(2)
    plt.plot(frac_num, rthin_f, marker='*', ms=12, color='b', label=r'$r_{0,thin}$')
    plt.plot(frac_num, zthin_f, marker='s', ms=8, color='r', label=r'$z_{0,thin}$')
    plt.plot(frac_num, rthick_f, marker='o', ms=10, color='g', label=r'$r_{0,thick}$')
    plt.plot(frac_num, zthick_f, marker='p', ms=10, color='k', label=r'$z_{0,thick}$')
    plt.plot(frac_num, ratio_f, marker='h', ms=10, color='c', label=r'$\frac{n_{thick}}{n_{thin}}$')
    plt.axis([0, Ntotal, 0, 0.5])
    plt.xlabel('Step Number')
    plt.ylabel(r'$\frac{|\sigma_{plus} - \sigma_{minus}|}{\sigma_{plus}}$', fontsize=24)
    plt.legend(loc=2)
    plt.savefig('convergence_' + str(Nsteps) + '.png')

if __name__ == '__main__':
    main()
