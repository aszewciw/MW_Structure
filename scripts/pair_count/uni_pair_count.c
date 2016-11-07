/*

Given a single bin min, a single bin max, and a uniform
sample, we record and write a file containing the pair
indices belonging to that bin.

*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* -------------------------------------------------------------------------- */
/* structure used to store the data set of particles */
typedef struct POINT{
  double x,y,z;
  double weight;
} POINT;

typedef struct DATA{
  unsigned int N;
  POINT *points;
} DATA;
/* -------------------------------------------------------------------------- */


int main(int argc, char **argv){

  if (argc != 4){
    fprintf( stderr, "Usage:\n %s file r_min r_max > outfile\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  FILE *file;

  if((file = fopen(argv[1],"r")) == NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }

  long double rmin, rmax;
  sscanf(argv[2], "%Lf", &rmin);
  sscanf(argv[3], "%Lf", &rmax);

  if(rmin >= rmax){
    fprintf(stderr,
	    "Error: rmin is greater than rmax. Nothing will be calculated. \n");
    exit(EXIT_FAILURE);
  }

  if(rmin == 0){
    rmin = 1e-3;
    fprintf(stderr, "Warning: Input rmin is 0, so it is set to 1e-3. \n");
  }


  fprintf(stderr, "file is: %s\n", argv[1]);

  fprintf(stderr, "Start reading file. \n");

  int k;

  DATA data;

  /* first read in the length of the list */
  fscanf(file, "%d", &data.N);

  /* Claim an array */
  data.points = (POINT *)calloc(data.N, sizeof(POINT));
  int i, j;
  for(i = 0; i < data.N; i++){
      fscanf(file, "%lf", &data.points[i].x);
      fscanf(file, "%lf", &data.points[i].y);
      fscanf(file, "%lf", &data.points[i].z);
      fscanf(file, "%lf", &data.points[i].weight);
  }

  fclose(file);

  fprintf( stderr, "Done reading %s. %d particles read. \n", argv[1], data.N );

  fprintf(stderr, "Start counting pairs... \n");

  double rs1 = rmin * rmin;
  double rs2 = rmax * rmax;

  double dx, dy, dz, ds;

  POINT p1, p2;

  for(i = 0; i < data.N; i++){

    p1 = data.points[i];

    for(j = i + 1; j < data.N; j++){

      p2 = data.points[j];

      dx = fabs(p1.x - p2.x);
      if(dx >= rmax){
        continue;
      }

      dy = fabs(p1.y - p2.y);
      if(dy >= rmax){
        continue;
      }

      dz = fabs(p1.z - p2.z);
      if(dz >= rmax){
        continue;
      }

      ds = dx * dx + dy * dy + dz * dz; /* distance square */

      if(ds >= rs1 && ds < rs2){
        fprintf(stdout, "%d\t%d\n", i, j);
      }

    }
  }


  fprintf(stderr, "Done calculation and output. \n");

  free(data.points);
  return 0;
}