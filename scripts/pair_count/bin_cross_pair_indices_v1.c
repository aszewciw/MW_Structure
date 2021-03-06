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
  int *mod_ind;                                 /* array of pair indices */
  // int *N_rand;                                  /* number of randoms paired with each mod_ind */
  int *N_pairs;                         /* number of pairs */
} PAIRS;

/* ------------------------------------------------------------------------- */
void bin_pairs(POINT *, int, POINT *, int, PAIRS *, int);
void output_pairs(int, PAIRS *, int );
/* ------------------------------------------------------------------------- */

/* assign indices to appropriate bins */

void bin_pairs(POINT *model, int n_model, POINT *rand, int n_rand, PAIRS *pairs, int N_bins){

  double r1, r2, dx, dy, dz, ds2;

  int i, j, k;

  for(i = 0; i < n_model; i++){

    for(j = 0; j < n_rand; j++){

      /* get component differences */
      dx = model[i].x - rand[j].x;
      dy = model[i].y - rand[j].y;
      dz = model[i].z - rand[j].z;

      /* square of difference vector */
      ds2 = dx * dx + dy * dy + dz * dz;

      /* assign pair to correct bin */
      for(k = 0; k < N_bins; k++ ){

        r1 = pairs[k].r2_lower;
        r2 = pairs[k].r2_upper;
        if(ds2 >= r1 && ds2 < r2){
          pairs[k].N_pairs[i] += 1;
          break;
        }
      }
    }
  }
}

/* ------------------------------------------------------------------------- */
void output_pairs(int n_model, PAIRS *pairs, int n_bins){
  int k=0;
  unsigned int i;
  char out_filename[256];
  FILE *out_file;
  for(k=0; k<n_bins; k++){
    snprintf(out_filename, 256, "./pairs_bin_%d.dat", k);
    out_file = fopen(out_filename, "a");
    fprintf(out_file, "%d\n", n_model);
    for(i=0; i<n_model; i++){
      fprintf(out_file, "%d\t%d\n", pairs[k].mod_ind[i], pairs[k].N_pairs[i]);
    }
    fclose(out_file);
  }
}
/* ------------------------------------------------------------------------- */

int main(int argc, char **argv){

  if (argc != 4){
    fprintf( stderr, "Usage:\n %s model_file rand_file bins_file\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  FILE *model_file;

  if((model_file=fopen(argv[1],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }

  FILE *rand_file;

  if((rand_file=fopen(argv[2],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[2]);
    exit(EXIT_FAILURE);
  }

  FILE *bins_file;

  if((bins_file=fopen(argv[3],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[3]);
    exit(EXIT_FAILURE);
  }

  int n_model;

  /* first read in the length of the list */
  fscanf(model_file, "%d", &n_model);

  /* Claim an array */
  POINT *model;
  model = calloc(n_model, sizeof(POINT));
  int i;
  for(i = 0; i < n_model; i++){
    fscanf(model_file, "%lf", &model[i].x);
    fscanf(model_file, "%lf", &model[i].y);
    fscanf(model_file, "%lf", &model[i].z);
    fscanf(model_file, "%lf", &model[i].weight);
  }

  fclose(model_file);

  fprintf(stderr, "Done reading %s. %d particles read. \n", argv[1], n_model );

  /* first read in number of bins */
  int n_bins;
  fscanf(bins_file, "%d", &n_bins);

  PAIRS *pairs;
  pairs = malloc(n_bins * sizeof(PAIRS));

  int k;

  /*  read in bin settings and prepare corr */
  for(k = 0; k < n_bins; k++){
    fscanf(bins_file, "%lf", &pairs[k].r_lower);
    fscanf(bins_file, "%lf", &pairs[k].r_upper);
    fscanf(bins_file, "%lf", &pairs[k].r_middle);
    fscanf(bins_file, "%lf", &pairs[k].bin_size);
    pairs[k].r2_lower = pairs[k].r_lower * pairs[k].r_lower;
    pairs[k].r2_upper = pairs[k].r_upper * pairs[k].r_upper;
    pairs[k].N_pairs = malloc(n_model * sizeof(int));
    pairs[k].mod_ind = malloc(n_model * sizeof(int));
    for(i=0; i<n_model; i++){
      pairs[k].mod_ind[i] = i;
      pairs[k].N_pairs[i] = 0;
    }
  }

  fclose(bins_file);

  int n_rand;

  /* first read in the length of the list */
  fscanf(rand_file, "%d", &n_rand);

  /* Claim an array */
  POINT *rand;
  rand = calloc(n_rand, sizeof(POINT));
  for(i = 0; i < n_model; i++){
    fscanf(rand_file, "%lf", &rand[i].x);
    fscanf(rand_file, "%lf", &rand[i].y);
    fscanf(rand_file, "%lf", &rand[i].z);
    fscanf(rand_file, "%lf", &rand[i].weight);
  }

  fclose(rand_file);

  fprintf(stderr, "Done reading %s. %d particles read. \n", argv[2], n_rand );


  fprintf(stderr, "Start counting pairs... \n");

  bin_pairs(model, n_model, rand, n_rand, pairs, n_bins);

  fprintf(stderr, "Pairs binned. \n");

  output_pairs(n_model, pairs, n_bins);

  fprintf(stderr, "File output.\n");

  for(k = 0; k < n_bins; k++){
    free(pairs[k].mod_ind);
    free(pairs[k].N_pairs);
  }

  free(pairs);
  free(model);
  free(rand);

  return 0;
}