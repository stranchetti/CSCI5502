import json
import argparse
import numpy as np
import pickle
import bst

parser = argparse.ArgumentParser(description="Basic stats about a count JSON file")
parser.add_argument("-b", "--bst", help="Generate a Binary Search Tree pickle of repo ids that have at least COUNT events", metavar="COUNT", type=int, dest="thresh", default=0)
parser.add_argument("-o", "--output", help="Specify output pickle filename. Ignored unless -b is specified", default=None)
parser.add_argument("file", help="The JSON file, as output from jsoncounter.py or jsonmerger.py to analyze")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = json.loads(f.read())
    counts = [x for x in data.values()]
    #generate a tree of repos if we need to
    if args.thresh > 0:
        repos = bst.BST()
        for r, c in data.items():
            if c > args.thresh:
                #the conversion to JSON objects in our
                #jsoncounter.py/jsonmerger.py ends up turning
                #the repo id into a string (since it needs to be the
                #key in the JSON string), but its really an int
                repos.add(int(r))
        #get output filename
        out = args.output
        if out == None:
            out = args.file + "_" + str(args.thresh) + ".pickle"
        #write out pickle
        with open(out, "wb") as output_file:
            pickle.dump(repos, output_file)
        exit(0)
    np_counts = np.array(counts)
    print("Summary of events per repo:")
    print("\tNumber of repos:", len(np_counts))
    print("\tNumber of events:", np.sum(np_counts))
    print("\tMean:", np.mean(np_counts))
    print("\tStd deviation:", np.std(np_counts))
    print("\tmin:", np.amin(np_counts))
    print("\tQ1:", np.percentile(np_counts, 25))
    print("\tMedian:", np.median(np_counts))
    print("\tQ3:", np.percentile(np_counts, 75))
    print("\t90th percentile:", np.percentile(np_counts, 90))
    print("\t99th percentile:", np.percentile(np_counts, 99))
    print("\tmax:", np.amax(np_counts))
