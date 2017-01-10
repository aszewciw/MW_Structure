'''
Reads in todo_list containing info about cleaned SEGUE data. For each SEGUE
pointing a uniform sample of points is produced. The sample contains
"star_factor" times as many points as are in the SEGUE data sample. Here,
"star_factor" is passed via the command line. Thus, each pointing will have a
different number of stars.

The files produced are:
    uniform_<ID>.ascii.dat - ra,dec,distance,l,b,Z,R,x,y,z,weight(=1)
    uniform_<ID>.xyzw.dat - x,y,z,weight(=1)
'''
import mw_utilities_python.segue_star as seg
import sys, pickle, math, os, string, random
import numpy as np

#------------------------------------------------------------------------------
class Point():
    pass

#------------------------------------------------------------------------------
def random_unit(Ntot, pointing):
    """
    Generate random points for a given pointing in the sky.

    Keywords arguments:
    Ntot  -- Total number of random points needed.
    pointing -- A Pointing instance.

    Return a list of random points.
    Each element in the list is a Point instance, which should contain
    RA, Dec, distance, x, y, z, etc.
    """

    plate_size_cos = math.cos(seg.PLATE_RADIUS_RADIANS)

    center = (pointing.cartesian_x, pointing.cartesian_y, pointing.cartesian_z)

    random_sample = []

    while len(random_sample) < Ntot :

        aRandom = Point() # create a random point as a Point instance

        # generate a random number on [0,1]
        u = random.random()
        v = random.random()

        # Draw a random angular radius from the center for uniform distribution on a cap
        phi = math.acos(1 - u * (1 - plate_size_cos))

        # raise a vector from the center vector in Dec direction and get Cartesian coords
        ra = pointing.ra_rad
        dec = pointing.dec_rad + phi

        vec = seg.eq2cart(ra, dec, 1.0)

        # rotate the vector a random angle around the center axis vector,
        # using Rodrigues' formula

        theta = v * 2.0 * math.pi

        vec_rotated = seg.rodrigues(center, vec, theta)

        eq = seg.cart2eq(vec_rotated[0], vec_rotated[1], vec_rotated[2])

        aRandom.cartesian_x = vec_rotated[0]
        aRandom.cartesian_y = vec_rotated[1]
        aRandom.cartesian_z = vec_rotated[2]

        aRandom.ra_rad = eq[0]
        aRandom.dec_rad = eq[1]
        aRandom.distance = eq[2]

        aRandom.ra_deg = math.degrees(aRandom.ra_rad)
        aRandom.dec_deg = math.degrees(aRandom.dec_rad)

        #quickly check distance, should be 1
        if math.fabs(aRandom.distance - 1) > 1.0e-5:
            sys.stderr.write("Error: rotated vector is not unit!\n")

        #using dot product to check
        if seg.dot(vec_rotated, center) < plate_size_cos:
            sys.stderr.write("Warning: there is certainly something wrong..\n")
            sys.stderr.write("dot = {0}\t cos = {1}\n"
                             .format(seg.dot(cart, center), plate_size_cos))

        # append the generated random point to the list
        random_sample.append(aRandom)

    return random_sample

#--------------------------------------------------------------------------
def assign_distance(random_sample, r1, r2):
    """
    Assign distances to random points.
    Random points are distributed uniformly in a shell between [rmin, rmax].
    """
    if r2 <= r1:
        sys.stderr.write("Error: Cannot assign distance. "
                         "Shell parameters error.\n"
                         "The max radius smaller than the min.\n ")
        sys.exit()

    a = r1 ** 3
    b = r2 ** 3 - a

    for p in random_sample:

        u = random.random()

        p.distance = (u * b + a) ** (1.0 / 3.0)

    # recalculate the x, y, z of random points based on the assigned distance.
    for p in random_sample:
        p.cartesian_x, p.cartesian_y, p.cartesian_z = seg.eq2cart(p.ra_rad, p.dec_rad, p.distance)

    return random_sample

#--------------------------------------------------------------------------

def main():
    '''
    Generate random points according to a uniform distribution.

    Commands to be passed to this script:
        star_factor = N_uniform / N_segue (per each l.o.s.)
        todo_dir = directory containing todo_list
        out_dir = directory where we'll place uniform files
    '''
    # Parse CL
    elements_needed = int(4)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    star_factor = int(args_array[1])
    todo_dir    = args_array[2]
    out_dir     = args_array[3]

    # load the todo pointing list
    input_filename = todo_dir + 'todo_list.dat'
    sys.stderr.write('Loading pointing info from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Generating uniform samples..\n')
    sys.stderr.write('{} line-of-sight to generate..\n'.format(len(todo_list)))

    random.seed()

    # generate uniform sample and star sample for individual plates
    for p in todo_list:

        # a progress indicator
        if todo_list.index(p) % 10 == 0:
            sys.stderr.write('Generating #{} of {} ..\n'
                             .format(todo_list.index(p), len(todo_list)))

        if p.N_star == 0:
            sys.stderr.write('Error: Empty star list. \n')
            continue

        # total number of stars in each l.o.s.
        Ntot = p.N_star * star_factor

        # generate random numbers on a unit sphere
        random_sample = random_unit(Ntot, p)

        r1 = seg.INNER_DISTANCE_LIMIT
        r2 = seg.OUTER_DISTANCE_LIMIT

        # assign distance to random sample
        random_sample = assign_distance(random_sample, r1, r2)

        # calculate galactic coordinates for each points
        for i in random_sample:
            i.galactic_l_rad, i.galactic_b_rad = seg.eq2gal(i.ra_rad, i.dec_rad)
            i.galactic_l_deg = math.degrees(i.galactic_l_rad)
            i.galactic_b_deg = math.degrees(i.galactic_b_rad)
            i.galactic_Z, i.galactic_R = seg.gal2ZR(i.galactic_l_rad,
                i.galactic_b_rad, i.distance)

        # set random points' weight to 1
        for i in random_sample:
            i.weight = 1.0

        # output ascii format
        output_filename = out_dir + 'uniform_' + p.ID + '.ascii.dat'
        output_file = open(output_filename, "w")
        # first output the total number of points
        output_file.write('{}\n'.format(len(random_sample)))
        for i in random_sample:
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\t{4:.6e}\t{5:.6e}\t{6:.6e}\t{7:.6e}\t{8:.6e}\t{9:.6e}\t{10:.6e}\n'
                              .format(i.ra_rad, i.dec_rad, i.distance,
                                      i.galactic_l_rad, i.galactic_b_rad,
                                      i.galactic_Z, i.galactic_R,
                                      i.cartesian_x, i.cartesian_y, i.cartesian_z,
                                      i.weight))
        output_file.close()

        # output xyzw
        output_filename = out_dir + 'uniform_' + p.ID + '.xyzw.dat'
        output_file = open(output_filename, "w")
        # first output the total number of points
        output_file.write('{}\n'.format(len(random_sample)))
        for i in random_sample:
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(i.cartesian_x, i.cartesian_y, i.cartesian_z,
                                      i.weight)
                              )
        output_file.close()

        # output ZRw
        output_filename = out_dir + 'uniform_' + p.ID + '.ZRW.dat'
        output_file = open(output_filename, "w")
        # first output the total number of points
        output_file.write('{}\n'.format(len(random_sample)))
        for i in random_sample:
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\n'
                              .format(i.galactic_Z, i.galactic_R, i.weight)
                              )
        output_file.close()

    sys.stderr.write('Done. Uniform samples output to {} .\n'.format(out_dir))

if __name__ == '__main__' :
    main()

