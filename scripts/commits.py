from matplotlib import pyplot
import numpy as np
from scipy.stats import ttest_ind_from_stats
from glob import glob

class Summary(object):
    def __init__(self, n=None, mean=None, std=None,
                 min_val=None, q1=None, median=None,
                 q3=None, max_val=None):
        self.n = n
        self.mean = mean
        self.std = std
        self.min_val = min_val
        self.q1 = q1
        self.median = median
        self.q3 = q3
        self.max_val = max_val
    def __str__(self):
        return ("\tNumber of points: " + str(self.n) + "\n" + 
                "\tMean: " + str(self.mean) + "\n" + 
                "\tStd deviation: " + str(self.std) + "\n" +
                "\tmin: " +  str(self.min_val) + "\n" +
                "\tQ1: " + str(self.q1) + "\n" +
                "\tMedian: " + str(self.median) + "\n" +
                "\tQ3: " + str(self.q3) + "\n" +
                "\tmax: " + str(self.max_val)
        )

def summary(d):
    def _summary(scores):
        return Summary(len(scores), np.mean(scores), np.std(scores),
                       np.amin(scores), np.percentile(scores, 25),
                       np.median(scores), np.percentile(scores, 75),
                       np.amax(scores))
    data = np.array(d)
    total = _summary(data)
    #clean = data[np.where(data < total.q3 + 1.5 * (total.q3 - total.q1))]
    #clean_sum = _summary(clean)
    #out = data[np.where(data > total.q3 + 1.5 * (total.q3 - total.q1))]
    #out_sum = _summary(out)
    print("Using all data")
    print(total)
    #print("Data without outliers")
    #print(clean_sum)
    #print("Outliers only")
    #print(out_sum)
    #return [total, clean_sum, out_sum]
    return [total]

#med = []
#high = []
#with open("med.txt", "r") as f:
#    for l in f:
#        med.append(int(l))
#with open("high.txt", "r") as f:
#    for l in f:
#        high.append(int(l))
succ = []
for f in glob("results/commit_lengths/*_succ*"):
    print(f)
    succ.extend(np.loadtxt(f))
fail = []
for f in glob("results/commit_lengths/*_fail*"):
    print(f)
    fail.extend(np.loadtxt(f))

print("FAIL")
fail_sum = summary(fail)
print("SUCCESS")
succ_sum = summary(succ)

exit(1)

#for i, test in enumerate(["all", "clean", "outlier"]):
for i, test in enumerate(["all"]):
    stats = ttest_ind_from_stats(fail_sum[i].mean,
                                 fail_sum[i].std,
                                 fail_sum[i].n,
                                 succ_sum[i].mean,
                                 succ_sum[i].std,
                                 succ_sum[i].n,
                                 equal_var=False)
    #print(test + " data ttest: score=%f, pval=%f" % stats)
    print(stats)
    
#pyplot.subplot(1, 2, 1)
#pyplot.violinplot([med, high])
#pyplot.subplot(1, 2, 2)
#print(pyplot.boxplot([med, high]))
#pyplot.show()
