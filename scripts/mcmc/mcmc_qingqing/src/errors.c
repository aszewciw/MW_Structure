#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, int lower_ind, int upper_ind){

    int i, j;
    double chi2 = 0.0;
    double DD, MM, sigma2;

    for(i = lower_ind; i < upper_ind; i++){
        for(j = 0; j < p[i].N_bins; j++){
            DD = p[i].rbin[j].DD;
            MM = p[i].rbin[j].MM;
            sigma2 = p[i].rbin[j].sigma2;
            if (p[i].rbin[j].sigma2 == 0.0) continue;
            chi2 += (DD/MM - 1.0) * (DD/MM - 1.0) / sigma2;
        }
    }
    return chi2;
}

/* ----------------------------------------------------------------------- */

void calculate_sigma(POINTING *p, int lower_ind, int upper_ind){

    double tol = 1e-8;
    double sigmaDD, sigmaMM, DD, MM, f;
    int i, j;

    for(i = lower_ind; i < upper_ind; i++){
        /* loop over bin rows */
        for(j = 0; j < p[i].N_bins; j++){

            DD = p[i].rbin[j].DD;
            MM = p[i].rbin[j].MM;

            if( p[i].rbin[j].err_jk_DD<tol || DD<tol ){
                p[i].rbin[j].sigma2=0.0;
            }
            else if( p[i].rbin[j].err_jk_RR<tol || MM<tol ){
                p[i].rbin[j].sigma2=0.0;
            }
            else{
                sigmaDD = p[i].rbin[j].err_jk_DD * DD;
                sigmaMM = p[i].rbin[j].err_jk_RR * MM;
                f = DD / MM;
                p[i].rbin[j].sigma2 = f * f * ( (sigmaDD/DD)*(sigmaDD/DD)
                    + (sigmaMM/MM)*(sigmaMM/MM) );
            }
        }
    }
}