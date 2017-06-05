I haven't been properly including covariances. So this is me correcting it.

Briefly, what I now want to do is completely throw away measurements where dd=0.
How I'm going to do this is to, before I run the chain, check ALL data samples
for ANY cases where DD=0. Let's say bin3 in los4 has a dd of 0, in just one of
my samples. Then, I will not include measurements of dd for bin3, los4 when
calculating chi2 for ANY of my samples. In this way, no single sample has "more
information".

It's a bit tricky though, so what I have to do is check this information prior
to running the chain:

I have to eliminate the corresponding rows and columns ofmy correlation matrix
prior to inverting it.
I have to eliminate the measurements of DD, and repack a file in which the first
line is the integer number of bins used.
I have to eliminate the corresponding measurements of std_fid.
I have to rename the files for the binned pair indices for MM when I move them
to the proper folder.

I think that's all.