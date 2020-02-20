import sys
from matplotlib import pyplot as plt


fn = sys.argv[1]

def cdf(dat):
    i = 0
    indices, values = [], []
    while i < len(dat) - 1:

        val = dat[i]
        for s in range(12, -1, -1):
            while i + 2**s < len(dat) and dat[i + 2**s] == val:
                i += 2**s

        i += 1
        indices.append(i)
        values.append(val)

    return indices, values


with open(fn) as f:
    slices, types = list(map(int, f.readline().split()))
    data = list(map(int, f.readline().split()))

ix, vals = cdf(data)
plt.plot(vals, ix)
plt.show()

plt.hist(data, bins=30)
plt.show()
