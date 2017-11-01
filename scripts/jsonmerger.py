#!/usr/bin/env python3

import argparse
import json

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, required=True, help="output filename")
parser.add_argument("input", nargs="+", help="input filenames for files to merge")
args = parser.parse_args()

json_objects = []

for filename in args.input:
    try:
        in_file = open(filename, "r")
    except IOError:
        print("ERROR: File not found: \"" + filename + "\"")
        continue
    json_objects.append(json.load(in_file))
    in_file.close()

merged_counters = Counter()
for json_object in json_objects:
    merged_counters += json_object

out_file = open(args.output, "w")
json.dump(merged_counters, out_file)
out_file.close()
