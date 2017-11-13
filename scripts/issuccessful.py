#!/usr/bin/env python3

import argparse
import json

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--begin", nargs="+", help="")
parser.add_argument("-e", "--end", nargs="+", type=str, required=True, help="")
parser.add_argument("-s", "--success", type=str, required=True, help="")
parser.add_argument("-f", "--failure", type=str, required=True, help="")
args = parser.parse_args()

json_objects = []

for filename in args.begin:
    try:
        in_file = open(filename, "r")
    except IOError:
        print("ERROR: File not found: \"" + filename + "\"")
        continue
    json_objects.append(json.load(in_file))
    in_file.close()

begin_counter = Counter()
for json_object in json_objects:
    begin_counter += Counter(json_object)

json_objects = []

for filename in args.end:
    try:
        in_file = open(filename, "r")
    except IOError:
        print("ERROR: File not found: \"" + filename + "\"")
        continue
    json_objects.append(json.load(in_file))
    in_file.close()

end_counter = Counter()
for json_object in json_objects:
    end_counter += Counter(json_object)

success_file = open(args.success, "w")
failure_file = open(args.failure, "w")

begin_keys = begin_counter.keys()
end_keys = end_counter.keys()
for key in begin_keys():
    if key in end_keys:
        success_file.write(str(key) + "\n")
    else:
        failure_file.write(str(key) + "\n")

success_file.close()
failure_file.close()
