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
#include <omp.h>

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
    double dd_raw;  /* raw pair counts */
    double dd;      /* normalized pair counts */
} PAIRS;

/* -------------------------------------------------------------------------- */

void count_pairs( POINT *, int , PAIRS *, int );
double norm_pairs( POINT *, int );

/* -------------------------------------------------------------------------- */

/* count raw weighted pairs for each bin */
void count_pairs( POINT *data, int n_data, PAIRS *pairs, int N_bins ){

    #pragma omp parallel default(shared)
    {
        double r1, r2, dx, dy, dz, ds2, w_i, w_j;
        int i, j, k;
        double counts_private[N_bins];
        for(i=0; i<N_bins; i++) counts_private[i] = 0.0;

        #pragma omp for schedule(dynamic)
        for(i = 0; i < n_data; i++){

            for(j = 0; j < n_data; j++){

                if(i==j) continue;

                /* get component differences */
                dx = data[i].x - data[j].x;
                dy = data[i].y - data[j].y;
                dz = data[i].z - data[j].z;

                /* square of difference vector */
                ds2 = dx * dx + dy * dy + dz * dz;

                /* get weights */
                w_i = data[i].weight;
                w_j = data[j].weight;

                /* assign pair to correct bin */
                for(k = 0; k < N_bins; k++ ){

                    r1 = pairs[k].r2_lower;
                    r2 = pairs[k].r2_upper;
                    if(ds2 >= r1 && ds2 < r2){
                        // pairs[k].dd_raw += w_i * w_j;
                        /* add product to private counter */
                        counts_private[k] += w_i * w_j;
                        break;
                    }
                }
            }
        }
        #pragma omp critical
        for(k = 0; k < N_bins; k++) pairs[k].dd_raw += counts_private[k];
    }

    int k;
    for(k = 0; k < N_bins; k++) pairs[k].dd_raw /= 2.0;

    // for(i = 0; i < n_data; i++){

    //     for(j = i + 1; j < n_data; j++){

    //         /* get component differences */
    //         dx = data[i].x - data[j].x;
    //         dy = data[i].y - data[j].y;
    //         dz = data[i].z - data[j].z;

    //         /* square of difference vector */
    //         ds2 = dx * dx + dy * dy + dz * dz;

    //         w_i = data[i].weight;
    //         w_j = data[j].weight;

    //         /* assign pair to correct bin */
    //         for(k = 0; k < N_bins; k++ ){

    //             r1 = pairs[k].r2_lower;
    //             r2 = pairs[k].r2_upper;
    //             if(ds2 >= r1 && ds2 < r2){
    //                 pairs[k].dd_raw += w_i * w_j;
    //                 break;
    //             }
    //         }
    //     }
    // }
}

/* -------------------------------------------------------------------------- */

/* calculate normalization, the sum of the product of all weights */
double norm_pairs( POINT *data, int n_data ){

    double norm = 0.0;
    int i, j;

    #pragma omp parallel for default(shared) private(i,j) reduction(+:norm) \
    schedule(dynamic)
    for( i=0; i<n_data; i++ ){
        for( j=0; j<n_data; j++ ){
            if(i==j) continue;
            norm += data[i].weight*data[j].weight;
        }
    }

    // for( i=0; i<n_data; i++ ){
    //     for( j=0; j<n_data; j++ ){
    //         if(i==j) continue;
    //         norm += data[i].weight*data[j].weight;
        // }
    // }

    /* Divide by 2 because of double counting */
    norm /= 2.0;
    return norm;
}

/* -------------------------------------------------------------------------- */

int main(int argc, char **argv){

    if (argc != 3){
        fprintf( stderr, "Usage:\n %s data_file bins_file > outfile\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *data_file;

    if((data_file=fopen(argv[1],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
        exit(EXIT_FAILURE);
    }

      FILE *bins_file;

    if((bins_file=fopen(argv[2],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
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
        pairs[k].dd_raw = 0.0;
        pairs[k].dd = 0.0;
    }

    fclose(bins_file);

    /* load data file */
    int n_data;
    POINT *data;

    fprintf(stderr, "data file is: %s\n", argv[1]);
    fprintf(stderr, "Reading data .. \n");

    /* first read in the length of the list */
    fscanf(data_file, "%d", &n_data);

    /* Claim an array for a list of pointing */
    data = calloc(n_data, sizeof(POINT));

    for(i = 0; i < n_data; i++){
        fscanf(data_file, "%lf", &data[i].x);
        fscanf(data_file, "%lf", &data[i].y);
        fscanf(data_file, "%lf", &data[i].z);
        fscanf(data_file, "%lf", &data[i].weight);
    }

    fprintf(stderr, "Read %d stars. \n", n_data);

    fclose(data_file);

    /* calculate the correlation */
    fprintf(stderr, "Start calculating mock pair counts... \n");

    double normalization = norm_pairs(data, n_data);
    count_pairs(data, n_data, pairs, n_bins);

    /* output to file */
    fprintf(stdout, "# r_lower, r_upper, r_middle, bin_size, dd, dd_raw, norm\n");
    for(k = 0; k < n_bins; k++){
        /* get normalized pair counts */
        pairs[k].dd = pairs[k].dd_raw/normalization;
        fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%le\t%le\t%le\n",
            pairs[k].r_lower, pairs[k].r_upper, pairs[k].r_middle, pairs[k].bin_size,
            pairs[k].dd, pairs[k].dd_raw, normalization);
    }

    fprintf(stderr, "Done calculation and output. \n");


    return EXIT_SUCCESS;

}
