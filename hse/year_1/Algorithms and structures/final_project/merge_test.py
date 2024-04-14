from find_percentile import merge, bin_merge
from time import time
from copy import deepcopy
from random import randint
import numpy as np


def merge(a, b):
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    while i < len(a):
        result.append(a[i])
        i += 1
    while j < len(b):
        result.append(b[j])
        j += 1
    return result
def mergesort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = mergesort(a[:mid])
    right = mergesort(a[mid:])
    return merge(left, right)

m_time = []
binm_time = []

for i in range(6):
    print(f'Test {i}')
    a = [randint(-100, 101) for i in range(9*10**i, 9*10**(i+1))]
    b = [randint(-100, 101) for i in range(9*10**i, 9*10**(i+1))]
    a.sort()
    b.sort()
    print('a_len:', len(a), 'b_len:', len(b))

    a1 = deepcopy(a)
    b1 = deepcopy(b)

    t = time()
    c_merge = merge(a, b)
    m_time.append(time() - t)

    a1.extend(b1)
    t = time()
    a1 = mergesort(a1)
    binm_time.append(time() - t)

    print('Merge time:', np.mean(m_time))
    print('Bin_merge time:', np.mean(binm_time))
    #print(c_merge)
    #print(a1)
    assert c_merge == a1
    print(f'Test {i} was successful!')