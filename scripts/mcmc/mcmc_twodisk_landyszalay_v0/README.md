The starting point of this code was mcmc_twodisk_v1. Modifications were made
from that point as described below.

As opposed to the "natural estimator" of the two point correlation function
(DD/RR - 1), we here will use the "Landy-Szalay" estimator.

In more detail, the measurement on our data will be (DD - 2DR + RR)/RR, and the
measurement on our model will be (MM - 2MR + RR)/RR. Because we are not assuming
any errors in RR, however, when we do (data - model) / sigma, cancellation
leaves us with data = DD - 2DR, model = MM - 2MR, and sigma derived from a set
of 1000 fiducial mocks on which we calculate DD - 2DR.

The primary changes we need to make here:
1. We need DR counts in addition to DD counts.
2. The errors and covariances are for DD - 2DR.
3. In prepping the files, we need a set of randoms to calculate the relevant quantities.
4. We need binned files of the "MR" counts. This is actually just one column since the randoms are never weighted.
5. We need to normalize the MR counts appropriately. The correct normalization would be
the sum of all weights times the number of randoms.