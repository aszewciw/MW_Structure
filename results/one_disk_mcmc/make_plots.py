'''
A sample script to run an mcmc chain. We assume that all of the data has been
prepared in the "in_dir" folder. It outputs a file containing executable commands
used in the mock creations. This script is called by a bash script "test_mcmc.sh"
where passed parameters are specified.
'''
import mw_utilities_python as mwu
import sys, os
import numpy as np

def main():

    file_list = ['frac_cov.dat', 'frac_nocov.dat', 'nofrac_cov.dat', 'nofrac_nocov.dat']
    png_list  = ['frac_cov.png', 'frac_nocov.png', 'nofrac_cov.png', 'nofrac_nocov.png']
    cut_frac  = str(0.1)
    z0_thin_t = str(0.234)
    r0_thin_t = str(2.34)

    # get directories of scripts and executables
    scripts_dir = mwu.get_path.get_scripts_path()
    exe_file = scripts_dir + 'mcmc/plotting/params_contours_onedisk.py'

    for i in range(len(file_list)):
        f = file_list[i]
        p = png_list[i]
        cmd =   (
                'python ' + exe_file + ' ' + f + ' ' + p + ' '
                + cut_frac + ' ' + z0_thin_t + ' ' + r0_thin_t
                )

        os.system(cmd)

if __name__ == '__main__':
    main()
