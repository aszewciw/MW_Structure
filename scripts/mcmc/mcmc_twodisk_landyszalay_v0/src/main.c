#include "mcmc.h"
/*
Run an mcmc comparing model to data. Here, the data are selected g-dwarfs in the
SEGUE spectroscopic sample. The model is a two disk galaxy. The measurements
here are pair counts in different radial bins and for different pointings.

I should give more description but I'm lazy for now.

Options to add:
    1. do either covariance or non-covariance
    2. use scaled-fractional, fiducial, or jackknife errors
    3. do either one or two disks (possibly a halo?)
    4. better criteria for ending chain
    5. different estimators
*/

/*---------------------------------------------------------------------------*/
int main(int argc, char * argv[]){

    /* MPI initialization */
    int nprocs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    /*
    While optional arguments are parsed in the function below, we require info
    on the directories for input and output data.

    It would be preferable to make this its own function, but for now I'll leave
    it here.
    */
    int sanity_flag=0;
    int in_dir_length;
    int dd_dir_length;
    int cnt=1;

    /* check that we have directory names and string lengths */
    while(cnt<argc){
        if ( !strcmp(argv[cnt], "-fn") ){
            sanity_flag++;
        }
        else if ( !strcmp(argv[cnt], "-l_id") ){
            sanity_flag++;
            sscanf(argv[++cnt], "%d", &in_dir_length);
        }
        else if ( !strcmp(argv[cnt], "-id") )
            sanity_flag++;
        else if ( !strcmp(argv[cnt], "-l_dd") ){
            sanity_flag++;
            sscanf(argv[++cnt], "%d", &dd_dir_length);
        }
        else if ( !strcmp(argv[cnt], "-dd") )
            sanity_flag++;
        cnt++;
    }

    /* exit if we don't have directory info */
    if (sanity_flag!=5){
        fprintf(stderr, "Error! Check to make sure input and output directories (and the directory string lengths) are being passed.\n");
        exit(EXIT_FAILURE);
    }

    /* assign directory names */
    char out_filename[256];
    char in_dir[in_dir_length+1];
    char dd_dir[dd_dir_length+1];
    cnt = 1;
    while(cnt<argc){
        if (!strcmp(argv[cnt], "-fn")){
            snprintf(out_filename, 256, "%s", argv[++cnt]);
        }
        else if (!strcmp(argv[cnt], "-id")){
            snprintf(in_dir, in_dir_length+1, "%s", argv[++cnt]);
        }
        else if (!strcmp(argv[cnt], "-dd")){
            snprintf(dd_dir, dd_dir_length+1, "%s", argv[++cnt]);
        }
        cnt++;
    }

    /* parse command line for starting params, steps, and filename */
    ARGS cl_args = parse_command_line( argc, argv );

    if(rank==0){
        fprintf(stderr, "N_parameters: %d\n", cl_args.N_params);
        fprintf(stderr, "Starting parameters: r0_thin = %lf , z0_thin = %lf , r0_thick = %lf , z0_thick = %lf , ratio = %lf\n",
            cl_args.r0_thin, cl_args.z0_thin, cl_args.r0_thick, cl_args.z0_thick, cl_args.ratio);
        fprintf(stderr, "Results will be output to %s\n", out_filename);
    }

    /* -- Load data from various files --*/
    int i, j;
    int N_plist;
    POINTING *plist;

    /* have each process separately access these files */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank){
            load_pointingID(&N_plist, &plist, in_dir);
            if(rank == 0) fprintf(stderr, "%d pointings to do\n", N_plist);
        }
        MPI_Barrier(MPI_COMM_WORLD);
        current_rank++;
    }

    /* Establish slice of pointings for each process to handle */
    int slice_length;
    int remain = N_plist % nprocs;
    int lower_ind, upper_ind;

    /* Make slices as even as possible */
    slice_length = N_plist / nprocs;
    lower_ind = rank * slice_length;
    if (rank < remain){
        lower_ind += rank;
        slice_length++;
    }
    else lower_ind += remain;
    upper_ind = lower_ind + slice_length;

    /* Each process now loads data for its slice only */
    load_ZRW(plist, lower_ind, upper_ind, rank, in_dir);
    load_rbins(plist, lower_ind, upper_ind, rank, in_dir, dd_dir);
    load_pairs(plist, lower_ind, upper_ind, rank, in_dir);
    load_inv_correlation(plist, lower_ind, upper_ind, rank, in_dir);

    /* Run mcmc */
    run_mcmc(plist, cl_args, lower_ind, upper_ind, rank, nprocs, out_filename);

    /* Free allocated values */
    for(i=lower_ind; i<upper_ind; i++){
        for(j=0; j<plist[i].N_bins; j++){
            free(plist[i].rbin[j].MM_pair1);
            free(plist[i].rbin[j].MM_pair2);
            free(plist[i].rbin[j].MR_pair);
        }
        free(plist[i].rbin);
        free(plist[i].Z);
        free(plist[i].R);
        free(plist[i].weight);
    }
    free(plist);
    if(rank==0) fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return EXIT_SUCCESS;

}

/* ----------------------------------------------------------------------- */