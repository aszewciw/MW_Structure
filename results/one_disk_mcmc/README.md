# Test mcmc on a one-disk model.

## Here is a description of the data used:

    * Data: choose a set of parameters and generate one mock with same number/l.o.s. as cleaned SEGUE sample.
    * Model: choose another set of parameters and generate a mock with 10 times the stars per l.o.s. as data.
        * This is a "weighted" non-uniform set of points. When we move around parameter space in the mcmc, we reweight the points by weight_model/weight_fiducial.
    * Errors: choose another set of parameters and generate 1000 mocks. On each mock, perform pair counting and calculate mean, stdev, and correlation matrix.
        * As we move to a new set of parameters in the markov chain, we keep these errors constant. Thus, we assume that the stdev and corr matrix don't change.
        * We could use the same set of parameters as are used to generate the non-uniform model, but it seems like this may bias us.