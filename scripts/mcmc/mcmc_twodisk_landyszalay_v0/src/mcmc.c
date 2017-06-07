#include "mcmc.h"


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------  Functions called by MCMC  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* function used to set density weights */
double sech2(double x){
    return 1.0 / (cosh(x) * cosh(x));
}

/* ----------------------------------------------------------------------- */

/* Set weights for all model points based on disk parameters */
void set_weights(STEP params, POINTING *p, int lower_ind, int upper_ind){

    int i, j;

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < p[i].N_stars; j++){

            p[i].weight[j] = (
                ( sech2( p[i].Z[j] / (2.0 * params.z0_thin) )
                    * exp( -p[i].R[j] / params.r0_thin ) )
                + params.ratio *
                ( sech2( p[i].Z[j] / (2.0 * params.z0_thick) )
                    * exp( -p[i].R[j] / params.r0_thick ) ) );

            /* divide by fiducial */
            p[i].weight[j] /= p[i].weight_fid[j];
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MM counts */
double normalize_MM(double *weight, int N_stars){

    int i, j;
    double norm = 0.0;

    for(i = 0; i < N_stars; i++){

        for(j = 0; j < N_stars; j++){

            if(i == j) continue;

            norm += weight[i] * weight[j];
        }
    }
    norm /= 2.0;
    return norm;
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MR counts */
double normalize_MR(double *weight, int N_stars, int N_rand){

    int i;
    double norm = 0.0;

    for(i = 0; i < N_stars; i++) norm += weight[i];
    norm *= N_rand;
    return norm;
}

/* ----------------------------------------------------------------------- */

/* Calculate normalized model pair counts MM for 1 bin */
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2,
    double MM_norm, double *weight ){

    unsigned int i;
    double MM = 0.0;

    for(i = 0; i < N_pairs; i++) MM += weight[pair1[i]] * weight[pair2[i]];
    MM /= MM_norm;
    return MM;
}

/* ----------------------------------------------------------------------- */

/* Calculate normalized model pair counts MM for 1 bin */
double calculate_MR( unsigned int N_pairs, int *pair, double MR_norm, double *weight ){

    unsigned int i;
    double MR = 0.0;

    for(i = 0; i < N_pairs; i++) MR += weight[pair[i]];
    MR /= MR_norm;
    return MR;
}

/* ----------------------------------------------------------------------- */

/* Updates normalized values of MM for current model */
void update_model(POINTING *p, int lower_ind, int upper_ind){

    int i, j;
    double MM_norm, MR_norm;

    /* Loop over l.o.s. */
    for(i = lower_ind; i < upper_ind; i++){

        MM_norm = normalize_MM(p[i].weight, p[i].N_stars);
        MR_norm = normalize_MR(p[i].weight, p[i].N_stars, p[i].N_rand);

        for(j = 0; j < p[i].N_bins; j++){

            p[i].rbin[j].MM = calculate_MM( p[i].rbin[j].N_MM,
                p[i].rbin[j].MM_pair1, p[i].rbin[j].MM_pair2, MM_norm,
                p[i].weight );
            p[i].rbin[j].MR = calculate_MR( p[i].rbin[j].N_MR,
                p[i].rbin[j].MR_pair, p[i].rbin[j].MR_pair, MR_norm,
                p[i].weight );
            p[i].rbin[j].model = p[i].rbin[j].MM - 2*p[i].rbin[j].MR;
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Calculate degrees of freedom -- only do once */
int degrees_of_freedom(POINTING *p, int lower_ind, int upper_ind){

    int dof = 0;
    int i, j;

    for(i = lower_ind; i < upper_ind; i++){
        for(j = 0; j < p[i].N_bins; j++){
            if( p[i].rbin[j].DD == 0.0 ) continue;
            // if( p[i].rbin[j].std_fid == 0.0 ) continue;
            dof++;
        }
    }
    return dof;
}

/* ----------------------------------------------------------------------- */

/* Take a random step in parameter space */
void update_parameters(STEP c, STEP *n, gsl_rng * GSL_r){

    double delta;

    // double r0_thin_sigma  = 0.05;
    // double z0_thin_sigma  = 0.005;
    // double r0_thick_sigma = 0.05;
    // double z0_thick_sigma = 0.005;
    // double ratio_sigma    = 0.002;

    /* try alternate step sizes */
    double r0_thin_sigma = 0.2;
    double z0_thin_sigma = 0.005;
    double r0_thick_sigma = 0.1;
    double z0_thick_sigma = 0.005;
    double ratio_sigma = 0.02;

    /* change the position based on Gaussian distributions.  */
    delta = gsl_ran_gaussian(GSL_r, r0_thin_sigma);
    n->r0_thin = c.r0_thin + delta;

    delta = gsl_ran_gaussian(GSL_r, z0_thin_sigma);
    n->z0_thin = c.z0_thin + delta;

    delta = gsl_ran_gaussian(GSL_r, r0_thick_sigma);
    n->r0_thick = c.r0_thick + delta;

    delta = gsl_ran_gaussian(GSL_r, z0_thick_sigma);
    n->z0_thick = c.z0_thick + delta;

    /* avoid having ratio > 1 or < 0 */
    while(1){
        delta = gsl_ran_gaussian(GSL_r, ratio_sigma);
        n->ratio = c.ratio + delta;
        if(n->ratio < 1.0 && n->ratio >= 0.0) break;
    }

    /* Initialize chi2 values to 0 instead of nonsense */
    n->chi2 = 0.0;
    n->chi2_red = 0.0;
}


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MCMC --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Run mcmc chain */
void run_mcmc(POINTING *plist, ARGS args, int lower_ind, int upper_ind, int rank, int nprocs, char filename[256]){

    int i=0;                /* mcmc index */
    int eff_counter = 0;    /* number of accepted steps */
    double eff;             /* number accepted / total */
    STEP current;           /* current params */
    STEP new;               /* new mcmc parameters to test */
    double delta_chi2;      /* new - old chi2 */
    double tmp;             /* temp holder */
    int DOF = 0;            /* total degrees of freedom */
    int DOF_proc;           /* d.o.f. of each process */
    double chi2 = 0.0;      /* chi2 value for each process */

    if (rank == 0){
        fprintf(stderr, "Start MCMC chain. Max steps = %d\n", args.max_steps);
    }

    /* set first element with initial parameters from cl args */
    current.r0_thin  = args.r0_thin;
    current.z0_thin  = args.z0_thin;
    current.r0_thick = args.r0_thick;
    current.z0_thick = args.z0_thick;
    current.ratio    = args.ratio;
    current.chi2     = 0.0;
    current.chi2_red = 0.0;

    /* set initial weights of model points */
    set_weights(current, plist, lower_ind, upper_ind);
    if(rank==0) fprintf(stderr, "Initial weights set \n");

    /* get initial values of MM */
    update_model(plist, lower_ind, upper_ind);

    /* Calculate initial correlation value */
    chi2 = calculate_chi2(plist, current, args.cov, args.frac, lower_ind, upper_ind);
    MPI_Allreduce(&chi2, &current.chi2, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    /* Degrees of freedom never change -- calculate once */
    DOF_proc = degrees_of_freedom(plist, lower_ind, upper_ind);
    MPI_Allreduce(&DOF_proc, &DOF, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    DOF -= args.N_params;
    current.chi2_red = current.chi2 / (double)DOF;

    if(rank==0){
        fprintf(stderr, "Degrees of freedom is: %d\n", DOF);
        fprintf(stderr, "Chi2 value for intital params is %lf\n", current.chi2);
    }

    /* Define MPI type to be communicated */
    MPI_Datatype MPI_STEP;
    MPI_Datatype type[7] = { MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE,
        MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE };
    int blocklen[7] = { 1, 1, 1, 1, 1, 1, 1 };
    MPI_Aint disp[7];
    disp[0] = offsetof( STEP, r0_thin );
    disp[1] = offsetof( STEP, z0_thin );
    disp[2] = offsetof( STEP, r0_thick );
    disp[3] = offsetof( STEP, z0_thick );
    disp[4] = offsetof( STEP, ratio );
    disp[5] = offsetof( STEP, chi2 );
    disp[6] = offsetof( STEP, chi2_red );

    /* build derived data type */
    MPI_Type_create_struct( 7, blocklen, disp, type, &MPI_STEP );
    /* optimize memory layout of derived datatype */
    MPI_Type_commit(&MPI_STEP);

    /* define file for output and have proc 0 open */
    FILE *output_file;
    if(rank==0){
        output_file = fopen(filename, "a");
    }

    /* Initialize random number to be used in MCMC */
    const gsl_rng_type * GSL_T;
    gsl_rng * GSL_r;
    gsl_rng_env_setup();
    GSL_T = gsl_rng_default;
    GSL_r = gsl_rng_alloc(GSL_T);
    gsl_rng_set(GSL_r, time(NULL));

    /* mcmc */
    while(i<args.max_steps){
        /* Have only step 0 take random walk and send new params to all procs */

        if(rank==0 && i!=0) update_parameters(current, &new, GSL_r);
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Bcast(&new, 1, MPI_STEP, 0, MPI_COMM_WORLD);

        /* Set weights from new parameters */
        set_weights(new, plist, lower_ind, upper_ind);

        /* get new MM values */
        update_model(plist, lower_ind, upper_ind);

        /* Calculate and gather chi2 */
        chi2 = calculate_chi2(plist, new, args.cov, args.frac, lower_ind, upper_ind);
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Allreduce(&chi2, &new.chi2, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
        new.chi2_red = new.chi2 / (double)DOF;

        /* If new chi2 is better, accept step.
           If not, decide to accept/reject with some probability */
        /* Only rank 0 needs to do this */
        if(rank == 0){

            delta_chi2 = new.chi2 - current.chi2;

            if(delta_chi2 <= 0.0){
                current = new;
                eff_counter += 1;
            }
            else{
                tmp = (double)rand() / (double)RAND_MAX;
                if (tmp < exp( -delta_chi2 / 2.0 )){
                    current = new;
                    eff_counter += 1;
                }
                else{
                    /* use old positions */
                }
            }
            if(i % 1000 == 0){
                fprintf(stderr, "On step %d, accepted chi2 is %lf\n",
                    i, current.chi2);
                fprintf(stderr, "z0_thin: %lf, r0_thin: %lf, z0_thick: %lf, r0_thick: %lf, ratio: %lf\n",
                    current.z0_thin, current.r0_thin, current.z0_thick,
                    current.r0_thick, current.ratio);
            }
            output_mcmc(i, current, output_file);
            if(i % 50 == 0) fflush(output_file);
        }
        i+=1;
    }

    /* print lines indicating end of mcmc */
    if(rank==0){
        eff = (double)eff_counter / (double)args.max_steps;
        fclose(output_file);
        fprintf(stderr, "Efficiency of MCMC: %lf\n", eff);
        fprintf(stderr, "End MCMC calculation.\n");
    }
}