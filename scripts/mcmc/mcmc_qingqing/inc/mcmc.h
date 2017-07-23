#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>
#include <mpi.h>

/* Arguments optionally passed via command line */
typedef struct {
  double r0_thin;     /* initial thin disk scale length */
  double z0_thin;     /* initial thin disk scale height */
  double r0_thick;    /* initial thick disk scale length */
  double z0_thick;    /* initial thick disk scale height */
  double ratio;       /* initial thick:thin number density ratio */
  int N_params;       /* number of parameters */
  int max_steps;      /* max steps in MCMC chain */
  int frac;           /* set=1 if we want to use scaled fractional errors */
  int cov;            /* set=1 if we want to use covariance matrix */
} ARGS;

/* Store information about each step in the chain */
typedef struct {
  double r0_thin;     /* initial thin disk scale length */
  double z0_thin;     /* initial thin disk scale height */
  double r0_thick;    /* initial thick disk scale length */
  double z0_thick;    /* initial thick disk scale height */
  double ratio;       /* initial thick:thin number density ratio */
  double chi2;        /* total chi2 for step */
  double chi2_red;    /* chi2/DOF */
} STEP;

/* Data for each radial bin */
typedef struct {
  char binID[3];        /* ID for each radial bin */
  double DD;            /* segue pair counts */
  double MM;            /* model pair counts */
  double err_jk_DD;     /* fractional error in DD counts from jackknife */
  double err_jk_RR;     /* fractional error in RR counts from jackknife */
  double sigma2;        /* combined error in DD/MM, squared */
  unsigned int N_pairs; /* number of unique pairs */
  int * pair1;          /* array of pair1 index of length N_pairs */
  int * pair2;          /* array of pair2 index of length N_pairs */
} RBIN;

/* Inverted correlation matrix -- accessed as cor_row[i].cor_col[j] */
typedef struct {
  double * invcor_col; /* each column value corresponding to a row value */
} INVCOR;

/* Pointing line of sight in sky */
typedef struct {
  char ID[4];           /* Unique ID for pointing */
  int N_stars;          /* Number of stars in model sample */
  int N_bins;           /* Number of bins used for this los */
  double * Z;           /* array of star heights above gal plane */
  double * R;           /* array of star distances from gal center in gal plane */
  double * weight;      /* star's density weight based on Z, R */
  double * weight_fid;  /* this will just be 1.0 since we use randoms*/
  RBIN * rbin;          /* N_bins of these structures */
} POINTING;

/* I/O functions */
ARGS parse_command_line( int n_args, char ** arg_array );
void load_pointingID(int *N_plist, POINTING **plist, char in_dir[]);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank, char in_dir[]);
void load_rbins(POINTING *plist, int lower_ind, int upper_ind, int rank, char in_dir[], char dd_dir[]);
void load_pairs(POINTING *plist, int lower_ind, int upper_ind, int rank, char in_dir[]);
void output_mcmc(int index, STEP p, FILE *output_file);

/* Stats functions */
double calculate_chi2(POINTING *p, int lower_ind, int upper_ind);
void calculate_sigma(POINTING *p, int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP params, POINTING *p, int lower_ind, int upper_ind);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm,
  double *weight );
void update_model(POINTING *p, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int lower_ind, int upper_ind);
void update_parameters(STEP p, STEP *n, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, ARGS args, int lower_ind, int upper_ind, int rank, int nprocs, char filename[256]);

/* Other */
double sech2(double x);