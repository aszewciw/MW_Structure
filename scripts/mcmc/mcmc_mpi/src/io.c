#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  I / O data functions  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* check if we passed a filename, number of steps, or parameters */
ARGS parse_command_line( int n_args, char ** arg_array ){

    /* defaults */
    ARGS cl_args;
    cl_args.N_params = 5;
    cl_args.r0_thin  = 3.0;
    cl_args.z0_thin  = 0.3;
    cl_args.r0_thick = 4.0;
    cl_args.z0_thick = 1.2;
    cl_args.ratio    = 0.12;
    cl_args.max_steps = 100000;
    cl_args.min_steps = 30000;
    cl_args.std_steps = 10000;
    cl_args.tol  = 0.1;
    cl_args.frac = 0;
    cl_args.cov  = 0;

    int cnt = 1;
    while(cnt < n_args)
    {
        if ( !strcmp(arg_array[cnt],"-N_p") )
            sscanf(arg_array[++cnt], "%d", &cl_args.N_params);
        else if ( !strcmp(arg_array[cnt],"-rn") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.r0_thin);
        else if ( !strcmp(arg_array[cnt],"-zn") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.z0_thin);
        else if ( !strcmp(arg_array[cnt],"-rk") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.r0_thick);
        else if ( !strcmp(arg_array[cnt],"-zk") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.z0_thick);
        else if ( !strcmp(arg_array[cnt],"-a") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.ratio);
        else if ( !strcmp(arg_array[cnt],"-tol") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.tol);
        else if ( !strcmp(arg_array[cnt],"-max_s") )
            sscanf(arg_array[++cnt], "%d", &cl_args.max_steps);
        else if ( !strcmp(arg_array[cnt],"-min_s") )
            sscanf(arg_array[++cnt], "%d", &cl_args.min_steps);
        else if ( !strcmp(arg_array[cnt],"-std_s") )
            sscanf(arg_array[++cnt], "%d", &cl_args.std_steps);
        else if ( !strcmp(arg_array[cnt],"-frac") )
            sscanf(arg_array[++cnt], "%d", &cl_args.frac);
        else if ( !strcmp(arg_array[cnt],"-cov") )
            sscanf(arg_array[++cnt], "%d", &cl_args.cov);
        else if ( !strcmp(arg_array[cnt],"-fn") )
            cnt++;
        else if ( !strcmp(arg_array[cnt],"-l_id") )
            cnt++;
        else if ( !strcmp(arg_array[cnt],"-id") )
            cnt++;
        else if ( !strcmp(arg_array[cnt],"--help") || !strcmp(arg_array[cnt],"-h") ) {
            printf("Usage: ./run_mcmc [-fn <out_filename>] [-l_id <in_dir length>] [-id <in_dir>] [-N_p <n_params>] [-max_s <max_steps>] [-min_s <min_steps>]\n");
            printf("\t[-rn <r0_thin>] [-zn <z0_thin>] [-rk <r0_thick>] [-zk <z0_thick>] [-frac <frac>] [-cov <cov>]\n");
            printf("Defaults:\nN_p: 5\nrn: 3.0\nzn: 0.3\nrk: 4.0\nzk: 1.2\na: 0.12\nmin_s=30000\nmax_s=100000\nfrac: 0\ncov: 0\n");
            printf("No directory defaults exist. These must be passed!\n");
            exit(-1);
        }
        else{
            printf("\n***Error: Uncrecognized CL option %s\n\n", arg_array[cnt]);
            printf("Usage: ./run_mcmc [-fn <out_filename>] [-l_id <in_dir length>] [-id <in_dir>] [-N_p <n_params>] [-max_s <max_steps>] [-min_s <min_steps>]\n");
            printf("\t[-rn <r0_thin>] [-zn <z0_thin>] [-rk <r0_thick>] [-zk <z0_thick>] [-frac <frac>] [-cov <cov>]\n");
            printf("Defaults:\nN_p: 5\nrn: 3.0\nzn: 0.3\nrk: 4.0\nzk: 1.2\na: 0.12\nmin_s=30000\nmax_s=100000\nfrac: 0\ncov: 0\n");
            printf("No directory defaults exist. These must be passed!\n");
            exit(-1);
        }
        cnt++;
    }
    return cl_args;
}

/* ----------------------------------------------------------------------- */

/* Load unique ID of each pointing */
void load_pointingID(int *N_plist, POINTING **plist, char in_dir[]){

    char plist_filename[256];
    snprintf(plist_filename, 256, "%spointing_ID.dat", in_dir);

    FILE *plist_file;
    int N;
    POINTING *p;

    if((plist_file=fopen(plist_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", plist_filename);
        exit(EXIT_FAILURE);
    }

    /* First get length of list */
    fscanf(plist_file, "%d", &N);

    /* Claim array for list of pointings */
    p = calloc(N, sizeof(POINTING));

    /* Get pointing IDs */
    int i;
    for(i=0; i<N; i++){
        fscanf(plist_file, "%s", p[i].ID);
    }
    fclose(plist_file);

    /* Assign values to main function arguments */
    *N_plist = N;
    *plist = p;
}

/* ----------------------------------------------------------------------- */

/* Load number of bins. Bin edge values are not needed in chain. */
int load_Nbins(char in_dir[]){

    int N;
    char bin_filename[256];
    FILE *bin_file;
    snprintf(bin_filename, 256, "%srbins.ascii.dat", in_dir);
    if((bin_file=fopen(bin_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", bin_filename);
        exit(EXIT_FAILURE);
    }
    fscanf(bin_file, "%d", &N);
    fclose(bin_file);

    return N;
}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank, char in_dir[]){

    char zrw_filename[256];
    FILE *zrw_file;
    int i, j, N;
    double * Z;
    double * R;
    double * W;
    double * W_f;

    /* Read star data for each poiting */
    for(i = lower_ind; i < upper_ind; i++){

        snprintf(zrw_filename, 256, "%smodel_ZRW_%s.dat", in_dir, plist[i].ID);
        if((zrw_file=fopen(zrw_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", zrw_filename);
            exit(EXIT_FAILURE);
        }
        fscanf(zrw_file, "%d", &N); /* read in number of stars */

        /* Claim arrays */
        Z = calloc(N, sizeof(double));
        R = calloc(N, sizeof(double));
        W = calloc(N, sizeof(double));
        W_f = calloc(N, sizeof(double));

        /* Read file for zrw data */
        for(j=0; j<N; j++){
            fscanf(zrw_file, "%lf", &Z[j]);
            fscanf(zrw_file, "%lf", &R[j]);
            fscanf(zrw_file, "%lf", &W_f[j]);
        }

        fclose(zrw_file);

        /* Assign value to plist element */
        plist[i].N_stars = N;
        plist[i].Z = Z;
        plist[i].R = R;
        plist[i].weight = W;
        plist[i].weight_fid = W_f;
    }

    if(rank==0) fprintf(stderr, "Model data loaded from %s\n", in_dir);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank,
    char in_dir[])
{

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Loop over each pointing */
    for( i = lower_ind; i<upper_ind; i++ ){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        /* Also assign Bin ID */
        snprintf(filename, 256, "%sdd_%s.dat", in_dir, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for( j=0; j<N_bins; j++ ){
            fscanf(file, "%lf", &b[j].DD);
            snprintf(b[j].binID, 3, "%d", j);
        }
        fclose(file);

        /* load mean and standard deviation of pair counts for fiducial */
        snprintf(filename, 256, "%smean_std_%s.dat", in_dir, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%lf", &b[j].DD_fid);
            fscanf(file, "%lf", &b[j].std_fid);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    if(rank==0){
        fprintf(stderr, "DD counts loaded from %s\n", in_dir);
        fprintf(stderr, "Mean and standard deviation loaded from %s\n", in_dir);
    }
}

/* ----------------------------------------------------------------------- */

/* Load pairs for each bin in each l.o.s. */
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank,
    char in_dir[])
{

    char pair_filename[256];
    FILE *pair_file;
    int i, j;
    unsigned int k, N;
    int *pair1;
    int *pair2;

    /* Loop over each pointing */
    for(i=lower_ind; i<upper_ind; i++){

        for(j=0; j<N_bins; j++){
            snprintf(pair_filename, 256, "%spair_indices_p%s_b%s.dat", in_dir,
                plist[i].ID, plist[i].rbin[j].binID);
            if((pair_file=fopen(pair_filename,"r"))==NULL){
                fprintf(stderr, "Error: Cannot open file %s\n", pair_filename);
                exit(EXIT_FAILURE);
            }

            /* First get number of pairs */
            fscanf(pair_file, "%u", &N);

            /* Claim arrays */
            pair1 = calloc(N, sizeof(int));
            pair2 = calloc(N, sizeof(int));

            for(k=0; k<N; k++){
                fscanf(pair_file, "%d", &pair1[k]);
                fscanf(pair_file, "%d", &pair2[k]);
            }

            fclose(pair_file);

            /* Assign values to plist elements */
            plist[i].rbin[j].N_pairs = N;
            plist[i].rbin[j].pair1 = pair1;
            plist[i].rbin[j].pair2 = pair2;
        }

    }
    if(rank == 0)fprintf(stderr, "Pairs loaded from %s\n", in_dir);
}

/* ----------------------------------------------------------------------- */
/* load the inverted covariance matrix from mock pair counts */
void load_inv_correlation(POINTING *plist, int N_bins, int lower_ind, int upper_ind,
    int rank, char in_dir[])
{

    char invcor_filename[256];
    FILE *invcor_file;
    int i, j, k;
    INVCOR *row;
    double *col;

    /* Loop over each pointing */
    for(i=lower_ind; i<upper_ind; i++){

        /* First assign inverse correlation matrix terms */

        /* Claim space for bin data */
        row = calloc(N_bins, sizeof(INVCOR));

        /* read in file */
        snprintf(invcor_filename, 256, "%sinv_correlation_%s.dat", in_dir, plist[i].ID);
        if((invcor_file=fopen(invcor_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", invcor_filename);
            exit(EXIT_FAILURE);
        }

        /* loop over rows of corr matrix, reading in data */
        for(j=0; j<N_bins; j++){

            /* claim array for columns */
            col = calloc(N_bins, sizeof(double));

            for(k=0; k<N_bins; k++){
                fscanf(invcor_file, "%lf", &col[k]);
            }
            /* assign each column element to its row */
            row[j].invcor_col = col;
        }
        fclose(invcor_file);

        /* Assign values to plist elements */
        plist[i].invcor_row = row;
    }

    if(rank == 0)fprintf(stderr, "Correlation matrix loaded from %s\n", in_dir);
}

/* ----------------------------------------------------------------------- */

/* Output mcmc data to a file */
void output_mcmc(int index, ARGS p, FILE *output_file){

    /* Output column headers as first line */
    if(index==0){
        fprintf( output_file, "step\tchi2\tchi2_red\tr0_thin\tz0_thin\tr0_thick\tz0_thick\tratio\n");
    }

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_red, p.r0_thin, p.z0_thin,
        p.r0_thick, p.z0_thick, p.ratio );
}

/* ----------------------------------------------------------------------- */
