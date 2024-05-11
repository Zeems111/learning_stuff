import numpy as np
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel
from scipy.stats import t, binom, norm
import scipy.stats

s1 = (47, 48, 51, 52, 52, 50, 47, 46, 52, 48, 49, 55, 52, 49, 52, 47, 50, 53, 48, 52)
s2 = (60, 58, 61, 61, 54, 57, 59, 63, 60, 61)
t_stat, pvalue = ttest_ind(s1, s2, equal_var=False, alternative='two-sided')
#print(t_stat, pvalue)

x = np.mean(s1)
y = np.mean(s2)
#print(x, y)
'''var_x = np.var(s1, ddof = 1) / len(s1)
var_y = np.var(s2, ddof = 1) / len(s2)
std_t = np.sqrt(var_x + var_y)
t_stat = (x - y)/ std_t
print(t_stat)'''

binom_d = binom(n=10, p=3/4)
#print(binom_d.ppf(0.95))
p = 0
for i in [0, 1, 9, 10]:
    p += binom_d.pmf(i)
    #print(f'P(X == {i})', binom_d.pmf(i))
    #print(f'P(X <= {i})', binom_d.cdf(i))
    #print(f'P(X < {i})', binom_d.cdf(i-1))
    #print(f'P(X >= {i})', 1 - binom_d.cdf(i-1))
#print(p)
q = 0
for i in range(2,9):
    q += binom_d.pmf(i)
    #print(f'P(X == {i})', binom_d.pmf(i))
    #print(f'P(X <= {i})', binom_d.cdf(i))
    #print(f'P(X < {i})', binom_d.cdf(i-1))
    #print(f'P(X >= {i})', 1 - binom_d.cdf(i-1))
#print('P(not reject H0) is:', round(q, 8))
#print('Power of the test is:', round(1-q, 6))

#print(ttest_1samp([8,12,10,12,9], 12, alternative='greater'))

norm_d = norm(0, np.sqrt(0.05))
x_crit = norm_d.ppf(0.95)
#print('X_crit:', x_crit)

norm_d = norm(1, np.sqrt(0.05))
p = norm_d.cdf(x_crit)
#print('P(X <= x_crit):', p)
#print('Power of the test:', 1-p)

sample0 = (6, 7, 7, 5, 7, 8, 8, 7, 7, 7)
sample1 = (7, 6, 6, 5, 5, 6, 7, 5, 5, 8)
print(np.mean(sample0), np.mean(sample1))
print(np.var(sample0), np.var(sample1))
print(ttest_ind(sample0, sample1))
print(ttest_ind(sample0, sample1, equal_var=False))


sample0 = (6, 7, 7, 5, 7, 8, 8, 7, 7, 7)
sample1 = (7, 6, 6, 5, 5, 6, 7, 5, 5, 8)
t_stat, pvalue = ttest_ind(sample0, sample1, equal_var=False, alternative='two-sided')
#print(f'p-value is {pvalue}')

norm_d = norm(1, np.sqrt(0.05))

sample_size = 6
pop_mean = 3
pop_range = 4
mean_is_in = 0
for i in range(10000):
    sample = np.random.uniform(pop_mean - pop_range,
                            pop_mean + pop_range,
                            size=sample_size)

    std_err = np.std(sample, ddof=1)/np.sqrt(sample_size)
    r = 1.96 * std_err
    sample_mean = np.mean(sample)
    conf_int = (sample_mean - r, sample_mean + r)
    if conf_int[0] <= pop_mean <= conf_int[1]:
        mean_is_in += 1
#print(mean_is_in/10000)

#print(scipy.stats.t.interval(0.95, df=sample_size-1))

sample = (1,2,2,4,3,2,5)
n = len(sample)
sample_mean = np.mean(sample)
std_err = np.std(sample, ddof=1)/np.sqrt(n)
_, coef = scipy.stats.norm.interval(0.99)
print(sample_mean, coef, std_err, sample_mean + coef * std_err)

_, coef = scipy.stats.t.interval(0.99, df = n - 1)
print(sample_mean, coef, std_err, sample_mean + coef * std_err)

normis = scipy.stats.norm(0, 1)
print(normis.cdf(1.96))