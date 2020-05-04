#!/usr/bin/env python3

# python3 create-bw-plots.py "Bandwidth plot" /path/to/fingerprints/iat-{0,1,2,3,3-5}-ts.csv

import numpy as np
from matplotlib import pyplot as plt
from sys import argv, exit

if len(argv) < 3:
    print("Usage: create-bw-plots.py <title> <paths/to/csv>...")
    exit(1)

title = argv[1]

points = []
labels = []

for fn in argv[2:]:
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
plt.xlabel('Time to full page load (seconds)')
plt.ylabel('Fraction of pages that have loaded')
plt.title(title)

plt.axis([0, 60, 0.0, 1.0])
plt.savefig("bw.png")

plt.axis([5, 30, 0.1, 1.0])
plt.savefig("bw-trunc.png")
