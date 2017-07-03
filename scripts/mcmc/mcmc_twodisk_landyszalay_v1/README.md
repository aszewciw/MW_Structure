See mcmc_twodisk_landyszalay_v0 for more details. This new version does the
following:

For the MR pairs, we were previously writing and loading a file that wrote the
model index down each time it was paired with a random. So it looked like this:
0
0
0
0
0
1
1
1
...

This is stupid, so now I've changed things so that we load a file containing the
model index and the number of pairs it made with random points:
0 5
1 3
...