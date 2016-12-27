import mw_utilities_python as mwu
import sys, pickle, os
import subprocess

def main():

    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mock_dir = scripts_dir + 'prepare_points/prepare_mocks/'
    out_dir     = './mocks_data/'

    exe_file = mock_dir + 'bin/make_galaxy'
    Nprocs = 16
    Nmocks = 2

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isfile(exe_file):
        sys.stderr.write('{} does not exist. Making...'.format(exe_file))
        cmd = 'make -C ' + mock_dir
        os.system(cmd)

    cmd = ( 'time mpirun -n ' + str(Nprocs) + ' ' + exe_file + ' -N_m '
        + str(Nmocks)
        + ' -l_td ' + str(len(todo_dir)) + ' -td ' + todo_dir
        + ' -l_od ' + str(len(out_dir)) + ' -od ' + out_dir )
    # os.system(cmd)
    subprocess.run(cmd)

    cmd = ( 'python ' + mock_dir + '/clean_mocks.py ' + todo_dir + ' '
        + out_dir + ' ' + str(Nmocks) )
    os.system(cmd)

    cmd = 'rm ' + out_dir + 'temp*'
    os.system(cmd)

if __name__ == '__main__':
    main()
