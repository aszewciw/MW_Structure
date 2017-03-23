'''
Plot contours for chain output.
'''
import mw_utilities_python as mwu
import sys,os

def main():

    fname = './out_data/results.dat'
    plot_name = 'fidsig_nocov_nonuni_exclbin0.png'
    cut_frac  = '0.05'
    z0_thin_true  = '0.234'
    r0_thin_true  = '2.027'
    z0_thick_true = '0.675'
    r0_thick_true = '2.397'
    ratio_true    = '0.053'

    if not os.path.isfile(fname):
        sys.stderr.write('Error: {} does not exist.\n'.format(fname))
        sys.exit()

    scripts_dir = mwu.get_path.get_scripts_path()
    mcmc_dir = scripts_dir + 'mcmc/plotting/'
    exe_file = mcmc_dir + 'params_contours.py'

    if not os.path.isfile(exe_file):
        sys.stderr.write('Error: {} does not exist.\n'.format(exe_file))
        sys.exit()

    cmd = (
        'python ' + exe_file + ' ' + fname + ' ' + plot_name + ' ' + cut_frac
        + ' ' + z0_thin_true + ' ' + r0_thin_true + ' ' + z0_thick_true + ' '
        + r0_thick_true + ' ' + ratio_true
        )
    os.system(cmd)

if __name__ == '__main__':
    main()
