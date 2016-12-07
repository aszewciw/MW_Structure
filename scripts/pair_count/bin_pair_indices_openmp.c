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
#include <string.h>
#include <math.h>
#include <omp.h>

/* -------------------------------------------------------------------------- */

/* a single cartesian point */
typedef struct POINT{
    double x, y, z; /* cartesian coordinates */
    double weight;  /* chosen weight of correlation function */
} POINT;

/* info on radial bins */
typedef struct BINS{
    double r_lower, r_upper, r_middle, bin_size; /* bin dimensions */
    double r2_lower, r2_upper; /* squared bin edges */
} BINS;

/* info on pairs placed in corresponding bins of BINS structure */
typedef struct PAIRS{
    int * index1;    /* array of indices of first point in a pair */
    int * index2;    /* array of indices of second point in a pair */
    unsigned int N_pairs;   /* number of pairs for this bin */
} PAIRS;
/* -------------------------------------------------------------------------- */



/* -------------------------------------------------------------------------- */

/* concatenate two strings */
char* concat(char *s1, char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);//+1 for the zero-terminator
    //in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

/* -------------------------------------------------------------------------- */


/* count raw weighted pairs for each bin */
void bin_pairs( POINT *data, int n_data, BINS *bins, int N_bins ){

    /* temporary size of malloc'd arrays of pairs */
    unsigned int n_temp = n_data * n_data / N_bins;

    #pragma omp parallel default(shared)
    {
        double r1, r2, dx, dy, dz, ds2;
        int i, j, k;
        PAIRS *pairs = (PAIRS *)calloc(n_temp, sizeof(PAIRS));

        for(i=0; i<N_bins; i++){
            pairs[i].N_pairs = 0;
            pairs[i].index1 = calloc(n_temp, sizeof(int));
            pairs[i].index2 = calloc(n_temp, sizeof(int));
        }

        #pragma omp for schedule(dynamic)
        for(i = 0; i < n_data; i++){

            for(j = i + 1; j < n_data; j++){

                /* get component differences */
                dx = data[i].x - data[j].x;
                dy = data[i].y - data[j].y;
                dz = data[i].z - data[j].z;

                /* square of difference vector */
                ds2 = dx * dx + dy * dy + dz * dz;

                /* assign pair to correct bin */
                for(k = 0; k < N_bins; k++ ){

                    r1 = bins[k].r2_lower;
                    r2 = bins[k].r2_upper;
                    if(ds2 >= r1 && ds2 < r2){
                        /* add product to private counter */
                        pairs[k].index1[N_pairs] = i;
                        pairs[k].index2[N_pairs] = j;
                        pairs[k].N_pairs += 1;
                        break;
                    }
                }
            }
        }
        #pragma omp critical
        {
            for(i = 0; i < N_bins; i++){
                FILE *outfile;
                    char * outfile = concat(fpath, fname);

                // strcpy(cl_args.filename, "../data/mcmc_output/mcmc_result.dat");

            }

        }
    }

}

/* -------------------------------------------------------------------------- */

int main(int argc, char **argv){

    if (argc != 4){
        fprintf( stderr, "Usage:\n %s data_file bins_file out_dir\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *data_file;

    if((data_file=fopen(argv[1],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
        exit(EXIT_FAILURE);
    }

    FILE *bins_file;

    if((bins_file=fopen(argv[2],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[2]);
        exit(EXIT_FAILURE);
    }

    /* path to output directory */
    char * out_dir = argv[3];

    /* first read in number of bins */
    int n_bins;
    fscanf(bins_file, "%d", &n_bins);

    BINS *bins;
    bins = calloc(n_bins, sizeof(BINS));

    int i, k;

    /*  read in bin settings */
    for(k = 0; k < n_bins; k++){
        fscanf(bins_file, "%lf", &bins[k].r_lower);
        fscanf(bins_file, "%lf", &bins[k].r_upper);
        fscanf(bins_file, "%lf", &bins[k].r_middle);
        fscanf(bins_file, "%lf", &bins[k].bin_size);
        bins[k].r2_lower = bins[k].r_lower * bins[k].r_lower;
        bins[k].r2_upper = bins[k].r_upper * bins[k].r_upper;
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

    bin_pairs(data, n_data, bins, n_bins, out_dir);

    /* output to file */
    // fprintf(stdout, "# r_lower, r_upper, r_middle, bin_size, dd, dd_raw, norm\n");
    // for(k = 0; k < n_bins; k++){
    //     /* get normalized pair counts */
    //     pairs[k].dd = pairs[k].dd_raw/normalization;
    //     fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%le\t%le\t%le\n",
    //         pairs[k].r_lower, pairs[k].r_upper, pairs[k].r_middle, pairs[k].bin_size,
    //         pairs[k].dd, pairs[k].dd_raw, normalization);
    // }

    fprintf(stderr, "Done calculation and output. \n");


    return EXIT_SUCCESS;

}
