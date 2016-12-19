
from config import *

'''
Reads in todo_list containing info about cleaned SEGUE data.
Outputs the following:

( one of these for each pointing )
1. pickled star list (do I use this anywhere?)
2. xyzw ascii file for correlation function
3. ascii file containing all coordinates (used in mcmc/jackknife)
'''


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

    plate_size_cos = math.cos(PLATE_RADIUS_RADIANS) # the cos of the plate size

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

        vec = eq2cart(ra, dec, 1.0)

        # rotate the vector a random angle around the center axis vector,
        # using Rodrigues' formula

        theta = v * 2.0 * math.pi

        vec_rotated = rodrigues(center, vec, theta)

        eq = cart2eq(vec_rotated[0], vec_rotated[1], vec_rotated[2])

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
        if dot(vec_rotated, center) < plate_size_cos:
            sys.stderr.write("Warning: there is certainly something wrong..\n")
            sys.stderr.write("dot = {0}\t cos = {1}\n"
                             .format(dot(cart, center), plate_size_cos))

        # append the generated random point to the list
        random_sample.append(aRandom)

    return random_sample

#--------------------------------------------------------------------------

def assign_distance(random_sample, r1, r2):
    """
    Assign distances to random points.
    Random points are distributed uniformly in a shell between [rmin, rmax].
    """

    #
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
        p.cartesian_x, p.cartesian_y, p.cartesian_z = eq2cart(p.ra_rad, p.dec_rad, p.distance)

    return random_sample

#--------------------------------------------------------------------------

def main():

    # CL Input
    # star_factor = N_random / N_data in each l.o.s.
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    star_factor     = int(args_array[1])

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Generating random samples..\n')
    sys.stderr.write('{} line-of-sight to generate..\n'.format(len(todo_list)))

    # generate random sample and star sample for individual plates
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
        # Ntot = 2000
        # Ntot = 1500

        # generate random numbers on a unit sphere
        random_sample = random_unit(Ntot, p)

        r1 = INNER_DISTANCE_LIMIT
        r2 = OUTER_DISTANCE_LIMIT

        # assign distance to random sample
        random_sample = assign_distance(random_sample, r1, r2)

        # calculate galactic coordinates for each points
        for i in random_sample:
            i.galactic_l_rad, i.galactic_b_rad = eq2gal(i.ra_rad, i.dec_rad)
            i.galactic_l_deg = math.degrees(i.galactic_l_rad)
            i.galactic_b_deg = math.degrees(i.galactic_b_rad)
            i.galactic_Z, i.galactic_R = gal2ZR(i.galactic_l_rad,
                i.galactic_b_rad, i.distance)

        # set random points' weight to 1
        for i in random_sample:
            i.weight = 1.0

        # pickle output
        output_filename = data_dir + 'uniform_' + p.ID + '.dat'
        output_file     = open(output_filename, "wb")
        pickle.dump(random_sample, output_file)
        output_file.close()

        # output ascii format
        output_filename = data_dir + 'uniform_' + p.ID + '.ascii.dat'
        output_file = open(output_filename, "w")
        # first output the total number of points
        output_file.write('{}\n'.format(len(random_sample)))
        for i in random_sample:
            output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                              .format(i.ra_rad, i.dec_rad, i.distance,
                                      i.galactic_l_rad, i.galactic_b_rad,
                                      i.galactic_Z, i.galactic_R,
                                      i.cartesian_x, i.cartesian_y, i.cartesian_z,
                                      i.weight))
        output_file.close()

        # output xyzw
        output_filename = data_dir + 'uniform_' + p.ID + '.xyz.dat'
        output_file = open(output_filename, "w")
        # first output the total number of points
        output_file.write('{}\n'.format(len(random_sample)))
        for i in random_sample:
            output_file.write('{}\t{}\t{}\n'
                              .format(i.cartesian_x, i.cartesian_y, i.cartesian_z))
        output_file.close()


    sys.stderr.write('Done. Random samples output to {} .\n'.format(data_dir))

if __name__ == '__main__' :
    main()

