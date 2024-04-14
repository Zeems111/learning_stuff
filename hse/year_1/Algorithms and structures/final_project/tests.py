import numpy as np
from random import randint
from find_percentile import find_percentile, ordinal_rank
import itertools
from time import time
from copy import deepcopy
def reference_solution(a, b, p):
    c = []
    c.extend(a)
    c.extend(b)
    c.sort()
    #print('np_perc',np.percentile(c, p, method='inverted_cdf'))
    return np.percentile(c, p, method='inverted_cdf')

def best(a, b, p):
    merged_list = sorted(itertools.chain(a, b))
    k = ordinal_rank(len(a) + len(b), p)
    return merged_list[k - 1] if k else merged_list[0]
def tst_1():
    for i in range(6):
        print(f'Test {i}')
        a = [randint(-100, 101) for i in range(15*10**i)]
        b = [randint(-100, 101) for i in range(15*10**i)]
        print('a_len:', len(a), 'b_len:', len(b))
        a.sort()
        b.sort()
        np_time=[]
        best_time = []
        find_p_time = []
        for p in [10]:
            a1 = deepcopy(a)
            b1 = deepcopy(b)
            a2 = deepcopy(a)
            b2 = deepcopy(b)

            t = time()
            np_perc = true_percentile(a, b, p)
            np_time.append(time()-t)
            print('NumPy time:', np.mean(np_time))
            t = time()
            find_p_perc = find_percentile(a1, b1, p)
            find_p_time.append(time() - t)
            print('find_p time:', np.mean(find_p_time))

            t = time()
            best_perc = best(a2, b2, p)
            best_time.append(time() - t)
            print('best_time:', np.mean(best_time))
            assert np_perc == best_perc == find_p_perc




        print(f'Test {i} was successful!')


tst_1()