#!/usr/bin/bash

rm pair_count

gcc -Wall -xHost -O3 -vec_report2 pair_count.c -o pair_count
# icc -Wall -xHost -O3 -vec_report2 pair_count.c -o pair_count