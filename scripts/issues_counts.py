#!/usr/bin/env python3

import argparse
import pandas

from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+", help="Input files")
args = parser.parse_args()

results_success = defaultdict(lambda : defaultdict(float))
results_failure = defaultdict(lambda : defaultdict(float))

column_names = ['count','repo','month','comments','body','success']
for infile in args.files:
    data = pandas.read_csv(str(infile), header=None, delim_whitespace=True, names=column_names)
    months = data.month.unique() 
    for month in months:
        month_data_succ = data[(data.month == month) & (data.success == 1)]
        month_data_fail = data[(data.month == month) & (data.success == 0)]
        results_success[month]['body'] = month_data_succ.body.mean()
        print(results_success[month]['body'])
