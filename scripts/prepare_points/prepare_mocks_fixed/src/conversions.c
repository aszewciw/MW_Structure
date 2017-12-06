#include "config.h"

/*---------------------------------------------------------------------------*/

/* Galactic North Pole in J2000, in degrees! */
const double Galactic_North_Pole_RA = 192.859508;
const double Galactic_North_Pole_Dec = 27.128336;
const double Galactic_Ascending_Node = 32.932;
/* Default Sun's position */
const double Sun_R = 8.0;
const double Sun_Z = 0.0;

/*---------------------------------------------------------------------------*/

/* Get sun-star distance and return */
double get_distance(double Z, double R, double phi){

    double x, y, distance;

    /* Calculate in gal-centered coord. */
    x = R * cos(phi);
    y = R * sin(phi);

    /* Move to sun-centered */
    x += Sun_R;
    Z -= Sun_Z;

    distance = sqrt( x*x + y*y + Z*Z );

    return distance;
}

/*---------------------------------------------------------------------------*/

/* galaxy-centered Z, R, phi to sun-centered l, b */
/* Note that here, the x-axes are aligned */
void ZR_to_gal(STAR *s){

    /* These are cartesian values from the l, b system */
    double x_temp, y_temp, z_temp;

    /* Temporary gal centered x and y. Sun at y=0, x=-Sun_R */
    x_temp = s->gal_r * cos(s->gal_phi);
    y_temp = s->gal_r * sin(s->gal_phi);

    /* Move to sun-centered */
    x_temp += Sun_R;
    z_temp = s->gal_z - Sun_Z;

    /* Get l and b (distance already found in func above) */
    s->gal_l_rad = atan2(y_temp, x_temp);
    s->gal_b_rad = asin(z_temp / s->distance);

    if(s->gal_l_rad < 0.0) s->gal_l_rad += 2.0 * M_PI;
    s->gal_l_rad = fmod(s->gal_l_rad, (2.0 * M_PI));
}

/*---------------------------------------------------------------------------*/

/* update star's (ra, dec) using Galactic (l, b) */
void gal_to_eq(STAR *s){

    double alpha, delta, la;
    /* convert params to radians */
    alpha = Galactic_North_Pole_RA * M_PI / 180.0;
    delta = Galactic_North_Pole_Dec * M_PI / 180.0;
    la    = Galactic_Ascending_Node * M_PI / 180.0;

    double ra, dec, l, b;     /* temporary holders*/

    l = s->gal_l_rad;
    b = s->gal_b_rad;

    dec = asin(sin(b) * sin(delta) +
         cos(b) * cos(delta) * sin(l - la));

    ra = atan2(cos(b) * cos(l - la),
         sin(b) * cos(delta) - cos(b) * sin(delta) * sin(l - la)
         ) + alpha;

    if(ra < 0) ra += 2.0 * M_PI;

    ra = fmod(ra, (2.0 * M_PI));

    s->ra_rad = ra;
    s->dec_rad = dec;

}

/*---------------------------------------------------------------------------*/

/* update star's (x, y, z) using (ra, dec, distance)  */
void eq_to_cart(STAR *s){
    s->x = s->distance * cos(s->ra_rad) * cos(s->dec_rad);
    s->y = s->distance * sin(s->ra_rad) * cos(s->dec_rad);
    s->z = s->distance * sin(s->dec_rad);
}

/*---------------------------------------------------------------------------*/
