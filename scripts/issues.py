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
                results_succ[column[5:]][0] = month_data[column].iloc[0]
            elif 'fail' in column:
                results_fail[column[5:]][0] = month_data[column].iloc[0]

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
            results_succ[month][str(column) + '_mean'] = month_data_succ[column].mean()
            results_succ[month][str(column) + '_stddev'] = month_data_succ[column].std()
            results_fail[month][str(column) + '_mean'] = month_data_fail[column].mean()
            results_fail[month][str(column) + '_stddev'] = month_data_fail[column].std()

keys = list(results_succ.keys())
keys.remove("opened")
keys.remove("closed")
keys.remove("reopened")
keys.remove("count")
keys.sort(key=int)

for month in keys:
    print("\nMonth: " + str(month))
    for key in data_columns:
        print(key + ":")
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
        m1 /= nobs1
        m2 /= nobs2
        stddev1 /= nobs1
        stddev2 /= nobs2
        print("Success Scaled Mean: " + str(m1))
        print("Success Scaled StdDev: " + str(stddev1))
        print("Success Scaled Nobs: " + str(nobs1))
        print("Failure Scaled Mean: " + str(m2))
        print("Failure Scaled StdDev: " + str(stddev2))
        print("Failure Scaled Nobs: " + str(nobs2))
        print("Scaled T-Test: " + str(scipy.stats.ttest_ind_from_stats(m1,stddev1,nobs1,m2,stddev1,nobs2)))
        print()

m1=0
m2=0
stddev1=0
stddev2=0
nobs1=0
nobs2=0

print("\nUsing averaged means and stddev for the year")
for key in data_columns:
    print(key + ":")
    for month in keys:
        m1 += results_succ[month][key + "_mean"]
        m2 += results_fail[month][key + "_mean"]
        stddev1 += results_succ[month][key + "_stddev"]
        stddev2 += results_fail[month][key + "_stddev"]
        nobs1 += results_succ[month]["nobs"]
        nobs2 += results_fail[month]["nobs"]
    m1 /= len(keys)
    m2 /= len(keys)
    stddev1 /= len(keys)
    stddev2 /= len(keys)
    nobs1 /= len(keys)
    nobs2 /= len(keys)
    print("Success Mean: " + str(m1))
    print("Success StdDev: " + str(stddev1))
    print("Success Nobs: " + str(nobs1))
    print("Failure Mean: " + str(m2))
    print("Failure StdDev: " + str(stddev2))
    print("Failure Nobs: " + str(nobs2))
    print("T-Test: " + str(scipy.stats.ttest_ind_from_stats(m1,stddev1,nobs1,m2,stddev1,nobs2)))
    m1 /= nobs1
    m2 /= nobs2
    stddev1 /= nobs1
    stddev2 /= nobs2
    print("Success Scaled Mean: " + str(m1))
    print("Success Scaled StdDev: " + str(stddev1))
    print("Success Scaled Nobs: " + str(nobs1))
    print("Failure Scaled Mean: " + str(m2))
    print("Failure Scaled StdDev: " + str(stddev2))
    print("Failure Scaled Nobs: " + str(nobs2))
    print("Scaled T-Test: " + str(scipy.stats.ttest_ind_from_stats(m1,stddev1,nobs1,m2,stddev1,nobs2))+"\n")

print("Total Succ " + str(results_succ["count"][0]))
print("Opened Succ " + str(results_succ["opened"][0]))
print("Closed Succ " + str(results_succ["closed"][0]))
print("Reopened Succ " + str(results_succ["reopened"][0]))
print("Total Fail " + str(results_fail["count"][0]))
print("Opened Fail " + str(results_fail["opened"][0]))
print("Closed Fail " + str(results_fail["closed"][0]))
print("Reopened Fail " + str(results_fail["reopened"][0]))

print("Opened Succ/Total Succ " + str(results_succ["opened"][0]/results_succ["count"][0]))
print("Closed Succ/Total Succ " + str(results_succ["closed"][0]/results_succ["count"][0]))
print("Reopened Succ/Total Succ " + str(results_succ["reopened"][0]/results_succ["count"][0]))
print("Opened Fail/Total Fail " + str(results_fail["opened"][0]/results_fail["count"][0]))
print("Closed Fail/Total Fail " + str(results_fail["closed"][0]/results_fail["count"][0]))
print("Reopened Fail/Total Fail " + str(results_fail["reopened"][0]/results_fail["count"][0]))
