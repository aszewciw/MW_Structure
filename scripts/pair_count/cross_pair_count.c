/*

Performs a weighted pair counting on a set of data points occupying some volume.
That is to say, a "pair" for point i and j is i_weight*j_weight. Pairs are
normalized by the sum over all i,j (i!=j) of i_weight*j_weight. If no weight is
desired, then a value of 1.0 should be used.

Double precision is used in pair counting.

Input:
data file:
    first line - number of points/lines in file
    remaining lines - cartesian coordinates: x, y, z, weight
        * if no weight is desired to be used, then file should contain 1.0 for
          4th column
bins file:
    first line - number of bins/lines in file
    remaining lines - bin sizes in same units as data file:
        lower bin edge, upper bin edge, middle of bin, size of bin

Output:
(7 columns - should be redirected to desired file location)
    For each bin:
    lower bin edge, upper bin edge, middle of bin, size of bin,
    normalized pair counts, un-normed pair counts, normalization

*/

/* -------------------------------------------------------------------------- */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* -------------------------------------------------------------------------- */

/* a single cartesian point */
typedef struct POINT{
    double x, y, z; /* cartesian coordinates */
    double weight;  /* chosen weight of correlation function */
} POINT;

/* info on pairs for different radial bins */
typedef struct PAIRS{
    double r_lower, r_upper, r_middle, bin_size; /* bin dimensions */
    double r2_lower, r2_upper; /* squared bin edges */
    double dr_raw;  /* raw pair counts */
    double dr;      /* normalized pair counts */
} PAIRS;

/* -------------------------------------------------------------------------- */

void count_pairs( POINT *, int , POINT *, int , PAIRS *, int );
double norm_pairs( POINT *, int, POINT *, int );

/* -------------------------------------------------------------------------- */

/* count raw weighted pairs for each bin */
void count_pairs( POINT *data1, int n_data1, POINT *data2, int n_data2,
    PAIRS *pairs, int N_bins ){

    double r1, r2, dx, dy, dz, ds2, w_i, w_j;

    int i, j, k;

    for(i = 0; i < n_data1; i++){

        for(j = 0; j < n_data2; j++){

            /* get component differences */
            dx = data1[i].x - data2[j].x;
            dy = data1[i].y - data2[j].y;
            dz = data1[i].z - data2[j].z;

            /* square of difference vector */
            ds2 = dx * dx + dy * dy + dz * dz;

            w_i = data1[i].weight;
            w_j = data2[j].weight;

            /* assign pair to correct bin */
            for(k = 0; k < N_bins; k++ ){

                r1 = pairs[k].r2_lower;
                r2 = pairs[k].r2_upper;
                if(ds2 >= r1 && ds2 < r2){
                    pairs[k].dr_raw += w_i * w_j;
                    break;
                }
            }
        }
    }
}

/* -------------------------------------------------------------------------- */

/* calculate normalization, the sum of the product of all weights */
double norm_pairs( POINT *data1, int n_data1, POINT *data2, int n_data2 ){

    double norm=0.0;
    int i, j;

    for( i=0; i<n_data1; i++ ){
        for( j=0; j<n_data2; j++ ){
            norm += data1[i].weight*data2[j].weight;
        }
    }
    return norm;
}

/* -------------------------------------------------------------------------- */

int main(int argc, char **argv){

    if (argc != 4){
        fprintf( stderr, "Usage:\n %s data1_file data2_file bins_file > outfile\n",
            argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *data1_file;

    if((data1_file=fopen(argv[1],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
        exit(EXIT_FAILURE);
    }

    FILE *data2_file;

    if((data2_file=fopen(argv[2],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[2]);
        exit(EXIT_FAILURE);
    }

    FILE *bins_file;

    if((bins_file=fopen(argv[3],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[3]);
        exit(EXIT_FAILURE);
    }

    /* first read in number of bins */
    int n_bins;
    fscanf(bins_file, "%d", &n_bins);

    PAIRS *pairs;
    pairs = calloc(n_bins, sizeof(PAIRS));

    int i, k;

    /*  read in bin settings and prepare corr */
    for(k = 0; k < n_bins; k++){
        fscanf(bins_file, "%lf", &pairs[k].r_lower);
        fscanf(bins_file, "%lf", &pairs[k].r_upper);
        fscanf(bins_file, "%lf", &pairs[k].r_middle);
        fscanf(bins_file, "%lf", &pairs[k].bin_size);
        pairs[k].r2_lower = pairs[k].r_lower * pairs[k].r_lower;
        pairs[k].r2_upper = pairs[k].r_upper * pairs[k].r_upper;
        pairs[k].dr_raw = 0.0;
        pairs[k].dr = 0.0;
    }

    fclose(bins_file);

    /* load data1 file */
    int n_data1;
    POINT *data1;

    fprintf(stderr, "First data file is: %s\n", argv[1]);
    fprintf(stderr, "Reading data .. \n");

    /* first read in the length of the list */
    fscanf(data1_file, "%d", &n_data1);

    /* Claim an array for a list of pointing */
    data1 = calloc(n_data1, sizeof(POINT));

    for(i = 0; i < n_data1; i++){
        fscanf(data1_file, "%lf", &data1[i].x);
        fscanf(data1_file, "%lf", &data1[i].y);
        fscanf(data1_file, "%lf", &data1[i].z);
        fscanf(data1_file, "%lf", &data1[i].weight);
    }

    fprintf(stderr, "Read %d stars. \n", n_data1);

    fclose(data1_file);


    /* load data file */
    int n_data2;
    POINT *data2;

    fprintf(stderr, "Second data file is: %s\n", argv[2]);
    fprintf(stderr, "Reading data .. \n");

    /* first read in the length of the list */
    fscanf(data2_file, "%d", &n_data2);

    /* Claim an array for a list of pointing */
    data2 = calloc(n_data2, sizeof(POINT));

    for(i = 0; i < n_data2; i++){
        fscanf(data2_file, "%lf", &data2[i].x);
        fscanf(data2_file, "%lf", &data2[i].y);
        fscanf(data2_file, "%lf", &data2[i].z);
        fscanf(data2_file, "%lf", &data2[i].weight);
    }

    fprintf(stderr, "Read %d stars. \n", n_data2);

    fclose(data2_file);

    /* calculate the correlation */
    fprintf(stderr, "Start calculating cross pair counts... \n");

    double normalization = norm_pairs(data1, n_data1, data2, n_data2);
    count_pairs(data1, n_data1, data2, n_data2, pairs, n_bins);

    /* output to file */
    fprintf(stdout, "# r_lower, r_upper, r_middle, bin_size, dr, dr_raw, norm\n");
    for(k = 0; k < n_bins; k++){
        /* get normalized pair counts */
        pairs[k].dr = pairs[k].dr_raw/normalization;
        fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%le\t%le\t%le\n",
            pairs[k].r_lower, pairs[k].r_upper, pairs[k].r_middle, pairs[k].bin_size,
            pairs[k].dr, pairs[k].dr_raw, normalization);
    }

    fprintf(stderr, "Done calculation and output. \n");

    return EXIT_SUCCESS;
}
