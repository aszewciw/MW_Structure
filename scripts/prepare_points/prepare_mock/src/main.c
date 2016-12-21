#include "config.h"
/*
Produce a mock Milky Way sample according to a two-disk model. This code
requires some CL Input and accepts some additional optional CL input. This input
is passed via the flags listed below (pass --help for more info).

Required CL Input:
    -l_od   - length of output directory string
    -od     - string of output directory
    -l_td   - length of todo list directory string
    -td     - string of directory containing todo_list (see io.c)

Optional CL Input (see io.c for default values):
    -N_s    - number of stars in a temporary galaxy
    -rn     - thin disk scale length
    -zn     - thin disk scale height
    -rk     - thick disk scale length
    -zk     - thick disk scale height
    -a      - thick/thin number density ratio

Stars are created in a "temporary galaxy" of a user-defined number. We determine
how many stars "belong" to each disk, based on the disks' parameters. We then
create stars first for the thin disk, then for the thick disk. The stars are
first created w.r.t. the galactic center. Their coordinates are then transfered
to a sun-centered cartesian system. They are then assigned to the appropriate
pointing (if applicable) and output to that pointing's file. In other words, one
file is produced for each pointing. Once we have made all stars in the temporary
galaxy and separated them into the pointings, we check if we have created
"enough" stars for all pointings. The threshhold for each pointing is set by the
todo file. We continue to make temporary galaxies, only adding stars to those
pointings which need more, until all threshholds are satisfied.

This procedure over-produces stars. This is intentional so as to not
preferentially select stars belonging to the thin disk (since we write those
stars to file first). Thus, after we run the code "clean_mocks.py" to shuffle
and cut down the size of our sample.

Note: l.o.s. = "line of sight"; i.e., a SEGUE/SDSS plate/pointing
*/

/*---------------------------------------------------------------------------*/

int main( int argc, char **argv ){

    /*
    While optional arguments are parsed in the function below, we require info
    on the directory of the todo list (of pointing info) and the output
    directory. We will perform this sanity check here.

    It would be preferable to make this its own function, but for now I'll leave
    it here.
    */
    int sanity_flag=0;
    int todo_dir_length;
    int out_dir_length;
    int cnt=1;

    /* check that we have directory names and string lengths */
    while(cnt<argc){
        if ( !strcmp(argv[cnt], "-l_od") ){
            sanity_flag++;
            sscanf(argv[++cnt], "%d", &out_dir_length);
        }
        else if ( !strcmp(argv[cnt], "-od") )
            sanity_flag++;
        else if ( !strcmp(argv[cnt], "-l_td") ){
            sanity_flag++;
            sscanf(argv[++cnt], "%d", &todo_dir_length);
        }
        else if ( !strcmp(argv[cnt], "-td") )
            sanity_flag++;
        cnt++;
    }

    /* exit if we don't have directory info */
    if (sanity_flag!=4){
        fprintf(stderr, "Error! Check to make sure todo and output directories (and the directory string lengths) are being passed\n");
        exit(EXIT_FAILURE);
    }

    /* assign directory names */
    char out_dir[out_dir_length+1];
    char todo_dir[todo_dir_length+1];
    cnt = 1;
    while(cnt<argc){
        if (!strcmp(argv[cnt], "-od")){
            snprintf(out_dir, out_dir_length+1, "%s", argv[++cnt]);
        }
        else if (!strcmp(argv[cnt], "-td")){
            snprintf(todo_dir, todo_dir_length+1, "%s", argv[++cnt]);
        }
        cnt++;
    }

    /* parse optional command line inputs for starting params and Nstars */
    ARGS cl = parse_command_line( argc, argv );

    unsigned long int N_stars;

    /* different variables used in main */
    POINTING *plist;        /* a pointing structure */
    int N_plist;            /* number of l.o.s. */
    int loop_flag;          /* set = 0 when file creation complete */
    int pointings_in_need;  /* a progress checker */
    PARAMS params;          /* parameters for mock creation */
    time_t t;               /* initialization of random seed */
    int N_mock;             /* # of stars in current mock l.o.s. */
    int N_data;             /* desired # of stars in current l.o.s. */
    int i;                  /* for loop index */
    int loop_counter;       /* a progress checker */

    /* load info for different pointings */
    load_pointing_list(&N_plist, &plist, todo_dir);

    /* get info for mock */
    /* change this to CL input eventually */
    params.r0_thin = cl.r0_thin;
    params.z0_thin = cl.z0_thin;
    params.r0_thick = cl.r0_thick;
    params.z0_thick = cl.z0_thick;
    params.ratio = cl.ratio;
    N_stars = cl.N_stars;
    get_params(&params, N_stars);

    /* Allocate arrays for galactic coordinates */
    STAR * thin  = malloc(params.N_thin * sizeof(STAR));
    STAR * thick = malloc(params.N_thick * sizeof(STAR));

    /* initialize random seed */
    srand((unsigned) time(&t));

    /* Initialize for while loop */
    loop_flag    = 0;
    loop_counter = 0;

    /* create temp mocks until all l.o.s. are filled */
    while(loop_flag==0){

        /* re-initialize at each step */
        pointings_in_need = 0;
        loop_flag         = 1;

        /* Make thin and thick disks */
        generate_stars(thin, &params, 0);
        generate_stars(thick, &params, 1);

        /* Separate stars into appropriate l.o.s. */
        separate_sample(plist, thin, N_plist, params.N_thin, out_dir);
        separate_sample(plist, thick, N_plist, params.N_thick, out_dir);

        /* Check all l.o.s. to see if we have enough stars */
        for( i=0; i<N_plist; i++ ){

            N_mock = plist[i].N_mock;
            N_data = plist[i].N_data;

            if(N_mock<N_data){
                /* indicate that we need more stars */
                loop_flag         = 0;
                plist[i].flag     = 0;
                pointings_in_need += 1;
            }
            else{
                /* we don't need more stars for this l.o.s. */
                plist[i].flag = 1;
            }
        }

        /* update progress and output results to user */
        loop_counter +=1;
        fprintf(stderr, "We've run the loop %d times.\n", loop_counter);
        if (pointings_in_need != 0){
            fprintf(stderr, "%d pointings need more stars.\n", pointings_in_need);
            fprintf(stderr, "Making more stars. \n");
        }
        else fprintf(stderr, "All pointings have an adequate number of stars. \n");
    }

    /* Deallocate arrays */
    free(thin);
    free(thick);
    free(plist);
    fprintf(stderr, "Files Written. Arrays deallocated.\n");

    return 0;
}

/*---------------------------------------------------------------------------*/
