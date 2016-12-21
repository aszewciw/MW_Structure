#include "config.h"

/*---------------------------------------------------------------------------*/

/* Return a galactic height according to distribution */
double random_gal_Z(double z0, double pdf_norm, double z_min,
    double z_max)
{
    /*  hard to define these variables: they are steps in inverting
        the cdf to draw from the distribution */
    double cdf;         /* Cumulative distribution function */
    double b;           /* lower bound (see below) */
    double temp;        /* temporary term */
    double z;           /* magnitude of height */
    double plus_minus;  /* random assignment above or below gal plane */

    /* get a random z */
    cdf  = (double)rand() / (double)RAND_MAX;
    b    = tanh( z_min / (2.0 * z0) );
    temp = ( cdf / (pdf_norm * 2.0 * z0) ) + b;
    z    = atanh(temp) * 2.0 * z0;

    /* Generate + or - 1.0 */
    plus_minus = floor( 2.0 * (double)rand() / (double)RAND_MAX );
    plus_minus = plus_minus * 2.0 - 1.0;

    z *= plus_minus;
    return z;
}

/*---------------------------------------------------------------------------*/

/* Return distance in galactic plane */
double random_gal_R(double r0, double pdf_norm, double r_min, double r_max)
{
    /*  hard to define these variables: they are steps in inverting
        the cdf to draw from the distribution */
    double cdf;         /* Cumulative distribution function */
    double min_term;    /* lower bound (see below) */

    double const1, const2, const3;  /* temporary constants

    /* alternate method */
    cdf      = (double)rand() / (double)RAND_MAX;
    const1   = cdf/pdf_norm;
    const2   = const1 / -r0;
    min_term = exp(-r_min/r0)*(r_min+r0);
    const3   = min_term + const2;

    /* Find roots of equation with bisection */
    int max_steps = 100; /* avoid getting caught in inifite loop */
    int i = 0;
    double a, b, c, f_b, f_c;
    double tol = 0.00001;
    f_c = 1.0;
    a = r_min;
    b = r_max;

    while(fabs(f_c)>tol && i<max_steps){
        i+=1;
        c = (a+b)/2.0;

        f_c = exp(-c/r0)*(c+r0) - const3;
        f_b = exp(-b/r0)*(b+r0) - const3;

        if((f_c * f_b)>0) b = c;
        else a = c;
    }

    if(i==max_steps) fprintf(stderr, "Oh no! Took more than 100 steps to converge!\n");
    return c;
}
/*---------------------------------------------------------------------------*/

/* dot product of two unit vectors */
double dot_product(VECTOR v1, VECTOR v2){

    double dot;

    dot = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;

    return dot;
}

/*---------------------------------------------------------------------------*/

/* make a temporary number of stars */
void generate_stars( STAR *s, PARAMS *p, int disk_type ){

    double z0;                  /* disk scale height */
    double r0;                  /* disk scale length */
    double z0_pdf_norm;         /* PDF height normalization */
    double r0_pdf_norm;         /* PDF length normalization */
    unsigned long int i;        /* loop variable...obvi */
    unsigned long int N_stars;  /* number of stars in disk */

    /* parse disk_type to decide if thin or thick */
    if(disk_type==0){
        /* use thin disk */
        N_stars     = p->N_thin;
        z0          = p->z0_thin;
        r0          = p->r0_thin;
        z0_pdf_norm = p->z0_pdf_norm_thin;
        r0_pdf_norm = p->r0_pdf_norm_thin;
    }
    else if(disk_type==1){
        /* use thick disk */
        N_stars     = p->N_thick;
        z0          = p->z0_thick;
        r0          = p->r0_thick;
        z0_pdf_norm = p->z0_pdf_norm_thick;
        r0_pdf_norm = p->r0_pdf_norm_thick;
    }
    else{
        /* quit because we messed up, man! */
        fprintf(stderr, "Unrecognized disk type. Exiting.\n");
        exit(EXIT_FAILURE);
    }

    /* calculate the remaining star attributes */
    for( i=0; i<N_stars; i++ ){
        s[i].gal_z = random_gal_Z(z0, z0_pdf_norm, p->z_min, p->z_max);
        s[i].gal_r = random_gal_R(r0, r0_pdf_norm, p->r_min, p->r_max);
        s[i].gal_phi = ( ( (double)rand() / (double)RAND_MAX )
            * p->phi_range + p->phi_min );
        s[i].distance = get_distance(s[i].gal_z, s[i].gal_r, s[i].gal_phi);
        ZR_to_gal(&s[i]);
        gal_to_eq(&s[i]);
        eq_to_cart(&s[i]);
    }
}

/*---------------------------------------------------------------------------*/

/* assign stars to the appropriate l.o.s. and output file */
void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s){

    int i, k;               /* loop variable for pointings */
    unsigned long int j;    /* loop variable for stars */
    char filename[256];     /* temp output file name */
    FILE *file;             /* temp output file */
    VECTOR plate;           /* plate's unit vector */
    VECTOR point;           /* current star's unit vector */
    double dot_prod;        /* dot product for two above vectors */
    double plate_cos;       /* used to assign stars to pointings */

    /* Calculate limit for assigning star to pointing */
    plate_cos = cos( PLATE_RADIUS_DEG * M_PI / 180. );

    for(j=0; j<N_s; j++){

        /* skip if outside distance range */
        if( (s[j].distance < 1.0) || (s[j].distance > 3.0) ) continue;

        /* star unit vectors */
        point.x = s[j].x / s[j].distance;
        point.y = s[j].y / s[j].distance;
        point.z = s[j].z / s[j].distance;

        for(i=0; i<N_p; i++){

            /* skip this pointing if we have enough stars */
            if( p[i].flag == 1) continue;

            /* plate unit vector */
            plate.x = p[i].x;
            plate.y = p[i].y;
            plate.z = p[i].z;

            /* get dot product of unit vectors */
            dot_prod = dot_product(plate, point);

            /* check assignment to this pointing */
            if(dot_prod >= plate_cos){

                /* index of stored star */
                k = p[i].N_mock;

                // snprintf(filename, 256, "%stemp_mock_%s.xyzw.dat",
                //     out_dir, p[i].ID);
                // file = fopen(filename, "a");
                p[i].stars[k].x = s[j].x;
                p[i].stars[k].y = s[j].y;
                p[i].stars[k].y = s[j].y;

                /* add 1 to number of stars */
                p[i].N_mock+=1;
                /* write star to file */
                // output_star( file, s[j] );
                // fclose(file);

                /* resize if necessary */
                if(p[i].N_mock>=p[i].ssize){
                    p[i].ssize += p[i].N_data;
                    p[i].stars = realloc(p[i].stars, p[i].ssize * sizeof(VECTOR));
                    fprintf(stderr, "Reallocation occurred for pointing %s\n", p[i].ID);
                }
            }
        }
    }
}
/*---------------------------------------------------------------------------*/
