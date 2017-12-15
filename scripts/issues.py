#!/usr/bin/env python3

import argparse
import pandas
import scipy.stats

from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--types", nargs="+", help="Input type files")
parser.add_argument("-f", "--files", nargs="+", help="Input count files")
args = parser.parse_args()

results_succ = defaultdict(lambda : defaultdict(float))
results_fail = defaultdict(lambda : defaultdict(float))

# Results gathering for count files
column_names = ['count','repo','month','comments','body','success']
data_columns = ['count','comments','body']

for infile in args.files:
    data = pandas.read_csv(str(infile), header=None, delim_whitespace=True, names=column_names)
    months = data.month.unique() 
    for month in months:
        month_data_succ = data[(data.month == month) & (data.success == 1)]
        month_data_fail = data[(data.month == month) & (data.success == 0)]
        # Observation counts
        results_succ[month]['nobs'] = month_data_succ.shape[0]
        results_fail[month]['nobs'] = month_data_fail.shape[0]
        for column in data_columns:
            # Get data for body 
            results_succ[month][column + '_mean'] = month_data_succ[column].mean()
            results_succ[month][column + '_stddev'] = month_data_succ[column].std()
            results_fail[month][column + '_mean'] = month_data_succ[column].mean()
            results_fail[month][column + '_stddev'] = month_data_succ[column].std()


# Results gathering for types files
column_names = ['month','total_count','succ_count','fail_count','succ_opened','fail_opened','succ_closed','fail_closed','succ_reopened','fail_reopened']
data_columns = ['succ_count','fail_count','succ_opened','fail_opened','succ_closed','fail_closed','succ_reopened','fail_reopened']

for infile in args.types:
    data = pandas.read_csv(str(infile), header=None, delim_whitespace=True, names=column_names)
    months = data.month.unique() 
    for month in months:
        month_data = data[data.month == month]
        for column in data_columns:
            if 'succ' in column:
                results_succ[column[5:]] = month_data[column].iloc[0]

print(results_succ['count'])
