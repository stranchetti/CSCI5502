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
            # Get data 
            results_succ[month][column + '_mean'] = month_data_succ[column].mean()
            results_succ[month][column + '_stddev'] = month_data_succ[column].std()
            results_fail[month][column + '_mean'] = month_data_fail[column].mean()
            results_fail[month][column + '_stddev'] = month_data_fail[column].std()


# Results gathering for types files
type_column_names = ['month','total_count','succ_count','fail_count','succ_opened','fail_opened','succ_closed','fail_closed','succ_reopened','fail_reopened']
type_data_columns = ['succ_count','fail_count','succ_opened','fail_opened','succ_closed','fail_closed','succ_reopened','fail_reopened']

for infile in args.types:
    data = pandas.read_csv(str(infile), header=None, delim_whitespace=True, names=type_column_names)
    months = data.month.unique() 
    for month in months:
        month_data = data[data.month == month]
        for column in type_data_columns:
            if 'succ' in column:
                results_succ[column[5:]] = month_data[column].iloc[0]

for month in sorted(results_succ.keys()):
    print("Month: " + str(month))
    for key in data_columns:
        try:
            m1 = results_succ[month][key + "_mean"]
            m2 = results_fail[month][key + "_mean"]
            stddev1 = results_succ[month][key + "_stddev"]
            stddev2 = results_fail[month][key + "_stddev"]
            nobs1 = results_succ[month]["nobs"]
            nobs2 = results_fail[month]["nobs"]
            print("Success Mean: " + str(m1))
            print("Success StdDev: " + str(stddev1))
            print("Success Nobs: " + str(nobs1))
            print("Failure Mean: " + str(m2))
            print("Failure StdDev: " + str(stddev2))
            print("Failure Nobs: " + str(nobs2))
            print("T-Test: " + str(scipy.stats.ttest_ind_from_stats(m1,stddev1,nobs1,m2,stddev1,nobs2)))
        except:
            continue
