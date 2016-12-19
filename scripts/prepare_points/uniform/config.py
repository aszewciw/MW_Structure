import os, sys, math, random
import string, csv
import pickle
import numpy as np

class Point:
    pass

class Star:
    pass

class Pointing:
    pass

PLATE_RADIUS_DEGREES = 1.49 # the radius of the plate, in degrees
PLATE_RADIUS_RADIANS = math.radians(PLATE_RADIUS_DEGREES)

#control the inner and outer limit of the sample to be used.
INNER_DISTANCE_LIMIT = 1.0
OUTER_DISTANCE_LIMIT = 3.0

#------------------------------------------------------------------------------
def eq2cart(ra, dec, r):
    """
    Convert Equatorial coordinates to Cartesian coordinates.
    Return a tuple (x, y, z) in the same unit of the input distance.

    Keywords arguments:
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    r   -- Distance

    """

    x = r * math.cos(ra) * math.cos(dec)
    y = r * math.sin(ra) * math.cos(dec)
    z = r * math.sin(dec)

    return x, y, z
#------------------------------------------------------------------------------
def cart2eq(x, y, z):
    """
    Convert Cartesian coordinates to Equatorial coordinates

    Keywords arguments:
    x -- x coordinate
    y -- y coordinate
    z -- z coordinate

    Return a tuple (ra, dec, z):
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    r   -- Distance in the same unit of input (x, y, z)
    """

    r = math.sqrt(x * x + y * y + z * z)
    ra = math.atan2(y, x)
    ra = ra if ra >= 0 else (2.0 * math.pi + ra)
    dec = math.asin(z / r)

    return ra, dec, r
#------------------------------------------------------------------------------
# RA(radians),Dec(radians),distance(kpc) of Galactic center in J2000
Galactic_Center_Equatorial=(math.radians(266.40510), math.radians(-28.936175), 8.33)

# RA(radians),Dec(radians) of Galactic Northpole in J2000
Galactic_Northpole_Equatorial=(math.radians(192.859508), math.radians(27.128336))
Galactic_Ascending_Node = math.radians(32.932)
#------------------------------------------------------------------------------
def eq2gal(ra,dec):
    """
    Convert Equatorial coordinates to Galactic Coordinates in the epch J2000.

    Keywords arguments:
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)

    Return a tuple (l, b):
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)
    """

    alpha = Galactic_Northpole_Equatorial[0]
    delta = Galactic_Northpole_Equatorial[1]
    la = Galactic_Ascending_Node

    b = math.asin(math.sin(dec) * math.sin(delta) +
                  math.cos(dec) * math.cos(delta) * math.cos(ra - alpha))

    l = math.atan2(math.sin(dec) * math.cos(delta) -
                   math.cos(dec) * math.sin(delta) * math.cos(ra - alpha),
                   math.cos(dec) * math.sin(ra - alpha)
                   ) + la

    l = l if l >= 0 else (l + math.pi * 2.0)

    l = l % (2.0 * math.pi)

    return l, b
#------------------------------------------------------------------------------
def gal2eq(l, b):
    """
    Convert Galatic coordinates to Equatorial Coordinates in the epch J2000.

    Keywords arguments:
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)

    Return a tuple (ra, dec):
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    """

    alpha = Galactic_Northpole_Equatorial[0]
    delta = Galactic_Northpole_Equatorial[1]
    la = Galactic_Ascending_Node

    dec = math.asin(math.sin(b) * math.sin(delta) +
                    math.cos(b) * math.cos(delta) * math.sin(l - la))

    ra = math.atan2(math.cos(b) * math.cos(l - la),
                    math.sin(b) * math.cos(delta) -
                    math.cos(b) * math.sin(delta) * math.sin(l - la)
                    ) + alpha

    ra = ra if ra>=0 else (ra + math.pi * 2.0)

    ra = ra % (2.0 * math.pi)

    return ra, dec
#------------------------------------------------------------------------------
# sun's distance away from the galactic center
Galactic_Sun_Position = 8.0

def gal2ZR(l, b, distance):
    """
    Transfer helio-centered galactic coordinates to galactic center based
    z and r (cylinder coordinates).
    Used to put into the galactic disk model to calculate the density.

    Keywords arguments:
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)

    Return a tuple (Z, R):
    Z  -- absolute distance above/below the galactic disk
    R -- distance away from the galactic center axis
    """

    # z projection
    Z = abs(distance * math.sin(b))
    # Law of cosines
    x = distance * math.cos(b)
    y = Galactic_Sun_Position
    R = math.sqrt(x * x + y * y - 2.0 * x * y * math.cos(l))

    return Z, R
#------------------------------------------------------------------------------
def dot(vec1, vec2):
    """
    Calculate the dot producs of 2 vectors in 3D Cartesian space.

    Keywords arguments:
    vec1 -- First vector in (x, y, z)
    vec2 -- Second vector in (x, y, z)

    Returns:
    dp -- the result of dot product
    """
    if len(vec1) is not 3 or len(vec2) is not 3:
        sys.stderr.write("Error: Wrong vector dimenson for dot product.\n")
        sys.exit()

    a1, a2, a3 = vec1[0], vec1[1], vec1[2]
    b1, b2, b3 = vec2[0], vec2[1], vec2[2]

    dp = a1 * b1 + a2 * b2 + a3 * b3

    return dp
#------------------------------------------------------------------------------
def cross(vec1, vec2):
    """
    Calculate the cross producs of 2 vectors in 3D Cartesian space.

    Keywords arguments:
    vec1 -- First vector in (x, y, z)
    vec2 -- Second vector in (x, y, z)

    Returns:
    vec -- the result vector in (x, y, z)
    """
    if len(vec1) is not 3 or len(vec2) is not 3:
        sys.stderr.write("Error: Wrong vector dimenson for cross product.\n")
        sys.exit()

    a1, a2, a3 = vec1[0], vec1[1], vec1[2]
    b1, b2, b3 = vec2[0], vec2[1], vec2[2]

    x = a2 * b3 - a3 * b2
    y = a3 * b1 - a1 * b3
    z = a1 * b2 - a2 * b1

    return x, y, z
#------------------------------------------------------------------------------
def rodrigues(axis, vec, theta):
    """
    Rotate a vector around an axis in 3D Cartesian space
    using Rodrigues' rotation formula.

    Keywords arguments:
    axis -- The vector of the axis in (x, y, z)
    vec  -- The vector to be rotated in (x, y, z)
    theta -- The rotation angle in radians.

    Return:
    vrot -- The rotated vector in (x, y, z)
    """
    # in case axis vector is a unit vector, normalize it.
    x0, y0, z0 = axis[0], axis[1], axis[2]

    r0 = math.sqrt(x0 * x0 + y0 * y0 + z0 * z0)

    x0 /= r0
    y0 /= r0
    z0 /= r0

    a = (x0, y0, z0)
    # cross product and dot product
    cp = cross(a, vec)
    dp = dot(a, vec)

    # rotation
    x = (vec[0] * math.cos(theta) + cp[0] * math.sin(theta)
         + x0 * dp * (1 - math.cos(theta)))

    y = (vec[1] * math.cos(theta) + cp[1] * math.sin(theta)
         + y0 * dp * (1 - math.cos(theta)))

    z = (vec[2] * math.cos(theta) + cp[2] * math.sin(theta)
         + z0 * dp * (1 - math.cos(theta)))

    return x, y, z
#------------------------------------------------------------------------------
