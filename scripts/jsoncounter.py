#!/usr/bin/env python

import argparse
import json

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", default="", type=str, help="input file to be read in")
parser.add_argument("input", type=str, help="input file to be read in")
args = parser.parse_args()

if args.output == "":
    args.output = "".join(args.input.split('.')[:-1]) + "-out.json"

json_file = ""
try:
    in_file = open(args.input, "r")
except IOError:
    print("ERROR: File Not Found: \"" + args.input + "\"")
    exit(1)

results = Counter()

for line in in_file:
    json_contents = json.loads(line)
    results[json_contents["repo"]["id"]] += 1
in_file.close()

out_file = open(args.output, "w")
json.dump(results, out_file)
out_file.close()
