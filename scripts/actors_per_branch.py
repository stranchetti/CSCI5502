#!/usr/bin/env python3

import argparse
import numpy as np
import scipy.stats

def main(filenames):
    num_actors = []
    for filename in filenames:
        with open(filename) as f:
            num_actors.append([int(line.strip().split('\t')[2]) for line in f])
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            print('Comparing files {} and {}'.format(
                filenames[i], filenames[j]))
            print('mean a: {}'.format(np.mean(num_actors[i])))
            print('std a: {}'.format(np.std(num_actors[i])))
            print('mean b: {}'.format(np.mean(num_actors[j])))
            print('std b: {}'.format(np.std(num_actors[j])))
            print(scipy.stats.ttest_ind(
                num_actors[i], num_actors[j], equal_var=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True, nargs='+')
    args = parser.parse_args()
    main(args.file)

