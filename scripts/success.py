#!/usr/bin/env python3

import argparse
import pickle
import numpy as np

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--repos", default="year.pickle")
parser.add_argument("-t", "--threshold", type=int, default=6)
parser.add_argument("files", nargs="+")
args = parser.parse_args()

counters = [Counter() for _ in range(12)]

for file_name in args.files:
    with open(file_name, "r") as f:
        for line in f:
            l = line.split()
            freq = int(l[0])
            repo = l[1]
            month = int(l[2])
            counters[month - 1][repo] += freq

means = []
for c in counters:
    v = c.values()
    means.append(np.mean(list(v)))
print(means)
#avoid dividing by zero for now. we won't need this once
#we have counts for each month
mean = np.nanmean(means)
print(mean)

repos = pickle.load(open(args.repos, "rb"))
succ = {}
fail = {}
for r in repos.keys():
    counts = [c[r] for c in counters]
    #np.where() returns a tuple, just need the first element
    if len(np.where(counts > mean)[0]) > args.threshold:
        succ[r] = None
    else:
        fail[r] = None
s_len = len(succ)
f_len = len(fail)
r_len = len(repos)
print("{} successful repos ({}%)".format(s_len, float(s_len / r_len) * 100))
print("{} unsuccessful repos ({}%)".format(f_len, float(f_len / r_len) * 100))
pickle.dump(succ, open("success.pickle", "wb"))
pickle.dump(fail, open("fail.pickle", "wb"))
    
