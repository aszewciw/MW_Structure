#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, STEP c, int cov, int frac, int lower_ind, int upper_ind){

    int i, j, k;
    double chi2 = 0.0;
    double corr_model_j, corr_model_k;  /* model counts */
    double corr_data_j, corr_data_k;    /* data counts */
    double sigma_j, sigma_k;            /* standard deviations */
    double r_jk;                        /* elements of correlation matrix */
    double chi2_temp;

    for(i = lower_ind; i < upper_ind; i++){

        /* loop over bin rows */
        for(j = 0; j < p[i].N_bins; j++){

            /* loop over bin column elements */
            for(k = 0; k < p[i].N_bins; k++){

                /* check if covariance or non-covariance */
                if(cov==0){   /* non-covariance */
                    if(j!=k){
                        r_jk = 0.0; /* no chi2 contribution */
                        continue;
                    }
                    else{
                        r_jk = 1.0; /* chi2 contribution */
                    }
                }
                else{
                    r_jk = p[i].invcor_row[j].invcor_col[k];
                }

                /* Set definitions for model and data */
                corr_model_j = p[i].rbin[j].model;
                corr_data_j  = p[i].rbin[j].data;
                corr_model_k = p[i].rbin[k].model;
                corr_data_k  = p[i].rbin[k].data;

                if(frac==0){
                    /* use fiducial sigmas */
                    sigma_j = p[i].rbin[j].std_fid;
                    sigma_k = p[i].rbin[k].std_fid;
                }
                else{
                    /* use model-weighted fractional sigmas */
                    sigma_j = ( (p[i].rbin[j].std_fid / p[i].rbin[j].data_fid)
                        * p[i].rbin[j].model );
                    sigma_k = ( (p[i].rbin[k].std_fid / p[i].rbin[k].data_fid)
                        * p[i].rbin[k].model );
                }

                /* hopefully for instances where I use the corr matrix sigma is
                not 0...
                */
                if(sigma_j==0.0 || sigma_k==0.0){
                    chi2_temp=0.0;
                }
                else{
                    /* add contribution to chi2 from correlation matrix element */
                    chi2_temp = ( ( ( corr_data_j - corr_model_j ) / sigma_j )
                        * ( ( corr_data_k - corr_model_k ) / sigma_k ) * r_jk );
                }
                chi2 += chi2_temp;
            }
        }
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
