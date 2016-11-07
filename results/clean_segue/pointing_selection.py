#!/usr/bin/env python

import mw_utilities_python as mwu
import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string

#------------------------------------------------------------------------------
def main():

    cleaned_dir = mwu.get_path.get_cleandata_path()

    # load pointing list
    input_filename = cleaned_dir + 'pointing_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    pointing_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare files for correlation function calculation..\n')

    # a list store the pointings to be used in calculation
    todo_list = []

    for p in pointing_list:

        star_filename = cleaned_dir + 'gstar_' + p.ID + '.dat'
        # skip empty files
        if not os.path.isfile(star_filename):
            continue
        if os.path.getsize(star_filename) == 0:
            continue

        with open(star_filename, 'rb') as star_file:
            star_list = pickle.load(star_file)

        # calculate the weights
        for s in star_list:
            s.weight = s.r_mag_weight_sn10 * s.type_weight_sn10

        # only include star with non-zero weight
        star_list = [s for s in star_list if s.weight != 0]

        # do some selection
        if len(star_list) < 50:
            continue # skip pointing with very few stars

        # check if the stars are in range
        r1 = seg.INNER_DISTANCE_LIMIT
        r2 = seg.OUTER_DISTANCE_LIMIT
        rlist = [s.distance for s in star_list]
        if min(rlist) > r1 or max(rlist) < r2:
            continue # skip pointing with stars only in too narrow range

        # only use stars within the range
        star_list = [s for s in star_list if s.distance > r1 and s.distance < r2]

        # add the number of stars to the pointing object
        p.N_star = len(star_list)
        # store it into the todo list
        todo_list.append(p)

        # output ascii file for correlation function calculation
        output_filename = cleaned_dir + 'star_' + p.ID + '.xyzw.dat'
        output_file = open(output_filename, 'w')
        output_file.write('{}\n'.format(p.N_star))
        for s in star_list:
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(s.cartesian_x, s.cartesian_y, s.cartesian_z,
                                      s.weight)
                              )
        output_file.close()


    # output ascii todo list
    output_filename = cleaned_dir + 'todo_list.ascii.dat'
    output_file = open(output_filename, "w")
    # first output total number of pointings
    output_file.write('{}\n'.format(len(todo_list)))
    for p in todo_list:
        output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                          .format(p.ID, p.ra_deg, p.dec_deg, p.ra_rad, p.dec_rad,
                                  p.galactic_l_rad, p.galactic_b_rad,
                                  p.cartesian_x, p.cartesian_y, p.cartesian_z,
                                  p.N_star))

    output_file.close()
    sys.stderr.write('Ascii todo list output to {} .\n'.format(output_filename))

    # output pickled todo list
    output_filename = cleaned_dir + 'todo_list.dat'
    output_file = open(output_filename, 'wb')
    pickle.dump(todo_list, output_file)
    sys.stderr.write('Pickled todo list is output to {} .\n'.format(output_filename))

if __name__ == '__main__' :
    main()
