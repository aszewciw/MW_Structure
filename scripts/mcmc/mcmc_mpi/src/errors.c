#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, STEP c, int N_bins, int lower_ind, int upper_ind){

    int i, j, k;
    double chi2 = 0.0;
    double corr_model_j, corr_model_k;  /* model counts */
    double corr_data_j, corr_data_k;    /* data counts */
    double sigma_j, sigma_k;            /* standard deviations */
    double r_jk;                        /* elements of correlation matrix */
    double chi2_temp;

    for(i = lower_ind; i < upper_ind; i++){

        /* loop over bin rows */
        for(j = 0; j < N_bins; j++){

            /* loop over bin column elements */
            for(k = 0; k < N_bins; k++){

                /* skip any bins where we have 0 counts */
                if( p[i].rbin[j].DD == 0.0 ) continue;
                if( p[i].rbin[j].MM == 0.0 ) continue;
                if( p[i].rbin[k].DD == 0.0 ) continue;
                if( p[i].rbin[k].MM == 0.0 ) continue;

                /* check if covariance or non-covariance */
                if(c.cov==0){   /* non-covariance */
                    if(j!=k){
                        r_jk = 0.0; /* no chi2 contribution */
                    }
                    else{
                        r_jk = 1.0; /* chi2 contribution */
                    }
                }
                else{
                    r_jk = p[i].invcor_row[j].invcor_col[k];
                }

                /* Set definitions for model and data */
                corr_model_j = p[i].rbin[j].MM;
                corr_data_j  = p[i].rbin[j].DD;
                corr_model_k = p[i].rbin[k].MM;
                corr_data_k  = p[i].rbin[k].DD;

                if(c.frac==0){
                    /* use fiducial sigmas */
                    sigma_j = p[i].rbin[j].std_fid;
                    sigma_k = p[i].rbin[k].std_fid;
                }
                else{
                    /* use model-weighted fractional sigmas */
                    sigma_j = ( (p[i].rbin[j].std_fid / p[i].rbin[j].DD_fid)
                        * p[i].rbin[j].MM );
                    sigma_k = ( (p[i].rbin[k].std_fid / p[i].rbin[k].DD_fid)
                        * p[i].rbin[k].MM );
                }

                /* add contribution to chi2 from correlation matrix element */
                chi2_temp = ( ( ( corr_data_j - corr_model_j ) / sigma_j )
                    * ( ( corr_data_k - corr_model_k ) / sigma_k ) * r_jk );
                chi2 += chi2_temp;
            }
        }
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
