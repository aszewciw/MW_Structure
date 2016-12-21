import mw_utilities_python as mwu
import sys, pickle, os

def main():

    star_factor = 10

    todo_dir = mwu.get_path.get_cleandata_path()
    scripts_dir = mwu.get_path.get_scripts_path()
    uniform_dir = scripts_dir + 'prepare_points/uniform/'
    out_dir     = './data/'

    if not os.path.isdir(out_dir):
        sys.stderr.write('{} does not exist. Making directory...'.format(out_dir))
        cmd = 'mkdir ' + out_dir
        os.system(cmd)

    cmd = ( 'python ' + uniform_dir + 'generate_uniform.py ' + str(star_factor)
        + ' ' + todo_dir + ' ' + out_dir )
    os.system(cmd)

if __name__ == '__main__':
    main()
