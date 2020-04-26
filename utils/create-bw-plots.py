#!/usr/bin/env python3

# python3 create-bw-plots.py /path/to/fingerprints/iat-{0,1,2,3,3-5}-ts.csv

import numpy as np
from matplotlib import pyplot as plt
from sys import argv, exit

if len(argv) < 2:
    print("filename please")
    exit(1)

points = []
labels = []

for i in range(1, len(argv)):
    fn = argv[i]
    s = fn.rfind('/')
    e = fn.rfind('.')
    labels.append(fn[s+1:e-3].upper()) # e-3 -> remove -ts
    with open(fn, "r") as f:
        points.append(list(map(float, f.read().split("\n")[1:-1])))

num_bins = 1000

for i in range(len(points)):
    counts, bin_edges = np.histogram (points[i], bins=num_bins)
    cdf = np.cumsum (counts)
    plt.plot (bin_edges[1:], cdf/cdf[-1])

plt.legend(labels)
plt.savefig("bw.png")

plt.axis([4, 35, 0, 1])
plt.savefig("bw-trunc.png")
