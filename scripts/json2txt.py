#!/usr/bin/env python3

import argparse
import json

from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, default="__unk__", help="output filename")
parser.add_argument("input", type=str, help="input filename")
args = parser.parse_args()

try:
    in_file = open(args.input, "r")
except IOError:
    print("ERROR: File not found: \"" + filename + "\"")
    exit(1)

json_object = json.load(in_file)

if args.output != "__unk__":
    out_file = open(args.output, "w")
    for key in json_object.keys():
        out_file.write(str(key) + "\t" + str(json_object[key]) + "\n")
    out_file.close()

for key in json_object.keys():
    print(str(key) + "\t" + str(json_object[key]))
