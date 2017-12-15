#!/usr/bin/env python3

import argparse
import itertools
import numpy as np
from scipy.stats import ttest_ind_from_stats
from glob import glob


succ = []
for f in glob("results/pullreq_commits/*_succ.txt"):
    succ.extend(np.loadtxt(f))

fail = []
for f in glob("results/pullreq_commits/*_fail.txt"):
    fail.extend(np.loadtxt(f))

m1 = np.mean(succ)
std1 = np.std(succ)
num1 = len(succ)
m2 = np.mean(fail)
std2 = np.std(fail)
num2 = len(fail)


stats = ttest_ind_from_stats(m1, std1, num1, m2, std2, num2, equal_var=False)
print("Means:")
print("%f, %f\n" % (m1, m2))

print("Standard Deviation:")
print(std1, std2)
print()

print("Counts:")
print(num1, num2)
print()

print("T-test Results:")
print(stats)
