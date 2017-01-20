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
  double tol;         /* tolerance for ending chain */
  int N_params;       /* number of parameters */
  int max_steps;      /* max steps in MCMC chain */
  int min_steps;      /* min steps in chain */
  int std_steps;      /* number of steps over which std are calculated */
  int frac;           /* set=1 if we want to use scaled fractional errors */
  int cov;            /* set=1 if we want to use covariance matrix */
} ARGS;

/* Store information about each step in the chain */
typedef struct {
  double r0_thin;     /* initial thin disk scale length */
  double z0_thin;     /* initial thin disk scale height */
  double chi2;        /* total chi2 for step */
  double chi2_red;    /* chi2/DOF */
} STEP;

/* Store the standard deviations for Nsteps */
typedef struct {
  int N_steps;          /* number of steps over which std are calculated */
  double r0_thin_std;   /* std of accepted thin disk scale lengths */
  double z0_thin_std;   /* std of accepted thin disk scale heights */
  double * r0_thin;     /* arrays of N_steps values of each quantity */
  double * z0_thin;
  double tol;           /* tolerance (fraction) for ending chain */
} STD;

/* Data for each radial bin */
typedef struct {
  char binID[3];        /* ID for each radial bin */
  double DD;            /* segue pair counts */
  double MM;            /* model pair counts */
  double DD_fid;        /* normalized mean pair counts for fiducial */
  double std_fid;       /* normalized stdev of pair counts for fid */
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
  double * Z;           /* array of star heights above gal plane */
  double * R;           /* array of star distances from gal center in gal plane */
  double * weight;      /* star's density weight based on Z, R */
  double * weight_fid;  /* star's density weight based on Z, R */
  RBIN * rbin;          /* Nbins of these structures */
  INVCOR * invcor_row;  /* Inverted correlation matrix: first index is a row */
} POINTING;

/* I/O functions */
ARGS parse_command_line( int n_args, char ** arg_array );
void load_pointingID(int *N_plist, POINTING **plist, char in_dir[]);
int load_Nbins(char in_dir[]);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank, char in_dir[]);
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank, char in_dir[]);
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank, char in_dir[]);
void load_inv_correlation(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank, char in_dir[]);
void output_mcmc(int index, STEP p, FILE *output_file);

/* Stats functions */
double calculate_chi2(POINTING *p, STEP c, int cov, int frac, int N_bins,
  int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP params, POINTING *p, int lower_ind, int upper_ind);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm,
  double *weight );
void update_model(POINTING *p, int N_bins, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
void update_parameters(STEP p, STEP *n, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, ARGS args, int N_bins, int lower_ind,
  int upper_ind, int rank, int nprocs, char filename[256]);

/* Other */
double sech2(double x);