/*

Given a single bin min, a single bin max, and a uniform
sample, we record and write a file containing the pair
indices belonging to that bin.

*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* ------------------------------------------------------------------------- */

/* a single cartesian point */
typedef struct POINT{
  double x, y, z; /* cartesian coordinates */
  double weight;  /* chosen weight of correlation function */
} POINT;

/* info on pairs for different radial bins */
typedef struct PAIRS{
  double r_lower, r_upper, r_middle, bin_size;  /* bin dimensions */
  double r2_lower, r2_upper;                    /* squared bin edges */
  int *pair1, *pair2;                           /* array of pair indices */
  unsigned int N_pairs;                         /* number of pairs */
} PAIRS;

/* ------------------------------------------------------------------------- */
void bin_pairs(POINT *, int, PAIRS *, int, int);
void output_pairs(PAIRS *, int );
/* ------------------------------------------------------------------------- */

/* assign indices to appropriate bins */
void bin_pairs(POINT *data, int n_data, PAIRS *pairs, int N_bins, int Nfetch){

  double r1, r2, dx, dy, dz, ds2;

  int i, j, k, h;

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

        r1 = pairs[k].r2_lower;
        r2 = pairs[k].r2_upper;
        if(ds2 >= r1 && ds2 < r2){

          /* increment pair count and record indices */
          h = pairs[k].N_pairs;
          pairs[k].pair1[h] = i;
          pairs[k].pair2[h] = j;
          pairs[k].N_pairs += 1;

          /* check if we need more memory */
          if(pairs[k].N_pairs%Nfetch==0){
            unsigned int n = pairs[k].N_pairs + Nfetch;
            pairs[k].pair1 = realloc(pairs[k].pair1, n * sizeof(int));
            pairs[k].pair2 = realloc(pairs[k].pair2, n * sizeof(int));
            fprintf(stderr, "Reallocation occured for bin index %d\n", k);
          }
          break;
        }
      }
    }
  }
}

/* ------------------------------------------------------------------------- */
void output_pairs(PAIRS *pairs, int n_bins){
  int k=0;
  unsigned int i;
  char out_filename[256];
  FILE *out_file;
  for(k=0; k<n_bins; k++){
    snprintf(out_filename, 256, "./pairs_bin_%d.dat", k);
    out_file = fopen(out_filename, "a");
    fprintf(out_file, "%u\n", pairs[k].N_pairs);
    for(i=0; i<pairs[k].N_pairs; i++){
      fprintf(out_file, "%d\t%d\n", pairs[k].pair1[i], pairs[k].pair2[i]);
    }
    fclose(out_file);
  }
}
/* ------------------------------------------------------------------------- */

int main(int argc, char **argv){

  if (argc != 3){
    fprintf( stderr, "Usage:\n %s data_file bins_file\n", argv[0]);
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

  /* first read in number of bins */
  int n_bins;
  fscanf(bins_file, "%d", &n_bins);

  PAIRS *pairs;
  pairs = malloc(n_bins * sizeof(PAIRS));

  int k;

  int Nfetch = 100000;

  /*  read in bin settings and prepare corr */
  for(k = 0; k < n_bins; k++){
    fscanf(bins_file, "%lf", &pairs[k].r_lower);
    fscanf(bins_file, "%lf", &pairs[k].r_upper);
    fscanf(bins_file, "%lf", &pairs[k].r_middle);
    fscanf(bins_file, "%lf", &pairs[k].bin_size);
    pairs[k].r2_lower = pairs[k].r_lower * pairs[k].r_lower;
    pairs[k].r2_upper = pairs[k].r_upper * pairs[k].r_upper;
    pairs[k].N_pairs = 0;
    pairs[k].pair1 = malloc(Nfetch * sizeof(int));
    pairs[k].pair2 = malloc(Nfetch * sizeof(int));
  }

  fclose(bins_file);


  int n_data;

  /* first read in the length of the list */
  fscanf(data_file, "%d", &n_data);

  /* Claim an array */
  POINT *points;
  points = calloc(n_data, sizeof(POINT));
  int i;
  for(i = 0; i < n_data; i++){
    fscanf(data_file, "%lf", &points[i].x);
    fscanf(data_file, "%lf", &points[i].y);
    fscanf(data_file, "%lf", &points[i].z);
    fscanf(data_file, "%lf", &points[i].weight);
  }

  fclose(data_file);

  fprintf(stderr, "Done reading %s. %d particles read. \n", argv[1], n_data );

  fprintf(stderr, "Start counting pairs... \n");

  bin_pairs(points, n_data, pairs, n_bins, Nfetch);

  fprintf(stderr, "Pairs binned. \n");

  output_pairs(pairs, n_bins);

  fprintf(stderr, "File output.\n");

  for(k = 0; k < n_bins; k++){
    free(pairs[k].pair1);
    free(pairs[k].pair2);
  }

  free(pairs);
  free(points);

  return 0;
}