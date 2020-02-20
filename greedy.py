def ass(dat, t, eps):
    n = len(dat)
    Lm = [(0, [])]
    for i in range(1, n + 1):
        Li = merge(Lm, lsum(Lm, dat[i-1], i-1), t)
        Li = trim(Li, eps / n)
        Lm = Li
    return Li[-1]

def trim(ln, delta):
    ret = [ln[0]]
    for sum_, indices in ln[1:]:
        if (1 - delta) * sum_ >= ret[-1][0]:
            ret.append((sum_, indices))
    return ret

def lsum(ln, x, i):
    return [(val + x, [*ix, i]) for val, ix in ln]

def merge(left, right, t):
    l = r = 0
    ret = []
    while l < len(left) and r < len(right):
        if left[l][0] <= t or right[r][0] <= t:
            if left[l] < right[r]:
                ret.append(left[l])
                l += 1
            else:
                ret.append(right[r])
                r += 1
        else:
            break
    else:  # case when one list is exhausted but not the other
        ln, ix = right, r
        if l < len(left):
            ln, ix = left, l
        for val, ix in ln[ix:]:
            if val > t: break
            ret.append((val, ix))
    return ret

def greedy(dat, t, frac=2, eps=1e-5):
    s = 0
    which = []
    for i in range(len(dat) - 1, -1, -1):

        # do end with fpga
        if (t - s) / t < frac:
            residual, which_residual = ass(dat[:i], t - s, eps)
            which.extend(which_residual)
            s += residual
            break

        if dat[i] + s < t:
            s += dat[i]
            which.append(i)

    return s, which


import sys

with open(sys.argv[1]) as f:
    t, _ = list(map(int, f.readline().split()))
    dat = list(map(int, f.readline().split()))



params = {
    'a': {'frac': 1e-5, 'eps': 1e-5},
    'b': {'frac': 2,    'eps': 1e-5},
    'c': {'frac': 2,    'eps': 1e-5},
    'd': {'frac': 1e-3, 'eps': 1e-3},
    'e': {'frac': 1e-5, 'eps': 1   },
}[sys.argv[1].split('/')[-1][0]]

# for e: frac=1e-5, eps=1
# for d: frac=1e-4, eps=1e-2
s, ix = greedy(dat, t, **params)
print(f'top: {t}, found: {s}')

with open(sys.argv[2], 'w') as f:
    f.write(f'{len(ix)}\n')
    f.write(f'{" ".join(map(str, ix))}\n')
