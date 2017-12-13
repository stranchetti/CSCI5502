#!/usr/bin/env python3

import argparse
import getpass
import pickle
import numpy as np
import mysql.connector

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--repos", default="year.pickle")
parser.add_argument("-t", "--threshold", type=int, default=6)
parser.add_argument("-u", "--user", type=str, default="root")
parser.add_argument("-d", "--db", type=str, default="datamining")
parser.add_argument("files", nargs="+")
parser.add_argument("-p", "--pass", help="Specify that you wish to provide a password for use with the MySQL database connection", action="store_true", dest="passwd")
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

# Get password if user requests to use one
passwd = None
if args.passwd:
    passwd = getpass.getpass("Please enter password:")

# Establish connection
try:
    ctx = mysql.connector.connect(user=args.user, database=args.database, passwd=passwd, charset="utf8mb4")
except mysql.connector.Error as error:
    print("Establishing connection to MySQL server failed: %s" % error)
    exit(1)
print("Etablished connection to MySQL server")

# Get cursor for later operations
cursor = ctx.cursor()

try:
    cursor.execute("ALTER TABLE repos ADD success BOOLEAN")
except mysql.connector.Error as error:
    print("Error occurred while trying to add the success column to the repos table")
    ctx.rollback()
    cursor.close()
    exit(1)

# Set success values
for repoid in succ.keys():
    try:
        cursor.execute("UPDATE repos SET success=TRUE WHERE id=%d" % int(repoid))
    except mysql.connector.Error as error:
        print("Failed to add success for repoid %d" % int(repoid))

# Set failure values
for repoid in fail.keys():
    try:
        cursor.execute("UPDATE repos SET success=FALSE WHERE id=%d" % int(repoid))
    except mysql.connector.Error as error:
        print("Failed to add failure for repoid %d" % int(repoid))
