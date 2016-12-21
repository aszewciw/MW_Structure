import mw_utilities_python as mwu
import sys, pickle, os

def main():

    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    mock_dir = scripts_dir + 'prepare_points/prepare_mock/'
    out_dir     = './mock_data/'

    exe_file = mock_dir + 'bin/make_galaxy'

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    if not os.path.isfile(exe_file):
        sys.stderr.write('{} does not exist. Making...'.format(exe_file))
        cmd = 'make -C ' + mock_dir
        os.system(cmd)

    cmd = ( exe_file + ' -l_td ' + str(len(todo_dir)) + ' -td ' + todo_dir
        + ' -l_od ' + str(len(out_dir)) + ' -od ' + out_dir )
    os.system(cmd)

    cmd = 'python ' + mock_dir + '/clean_mocks.py ' + todo_dir + ' ' + out_dir
    os.system(cmd)

    cmd = 'rm ' + out_dir + 'temp*'
    os.system(cmd)

if __name__ == '__main__':
    main()
