Writing this on June 6, 2017. This version differs from v0 in two main ways.

First, I've deleted lines associated with criteria for ending the chain. The
criteria in v0 really aren't well-motivated, and I had just been ignoring them.
Thus, now the chain just runs for a set number of steps.

Second, I've now changed things such that every l.o.s. has a unique number of
used bins. Preparation for an MCMC now requires that the file containing DD
pair counts contains the number of used bins as its first line. It also requires
that the files containing binned model pair counts, the inverse covariance
matrix, and the mean and standard deviation of MM pair counts must reflect these
changes. See ../mcmc_prep/prepare_files_multi_data_correction.py for more info.