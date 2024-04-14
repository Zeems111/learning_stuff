from numpy import percentile
from math import ceil
from time import time
from random import seed, randint
from itertools import product


def reference_solution(a, b, p):
    c = []
    c.extend(a)
    c.extend(b)
    c.sort()
    return percentile(c, p, method='inverted_cdf')


def find_percentile(a, b, p):
    def ordinal_rank(array_len, percentage):
        return ceil(percentage / 100 * array_len)

    k = ordinal_rank(len(a) + len(b), p)
    if k == 0:
        if a and b:
            return min(a[0], b[0])
        if not a:
            return b[0]
        if not b:
            return a[0]

    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b) and len(result) < k:
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    if len(result) >= k:
        return result[k - 1]

    while i < len(a) and len(result) < k:
        result.append(a[i])
        i += 1
    if len(result) >= k:
        return result[k - 1]

    while j < len(b) and len(result) < k:
        result.append(b[j])
        j += 1

    return result[k - 1]


def test_find_percentile(a, b, p, correct_answer):
    result = find_percentile(a, b, p)
    error_str = (f'Test failed!\n'
                 f'a: {a}\n'
                 f'b: {b}\n'
                 f'Result: {result}\n'
                 f'Correct answer: {correct_answer}')
    assert result == correct_answer, error_str
    print('Unit test - SUCCESS.')


def run_unit_tests():
    test_find_percentile([], [1], 50, 1)
    test_find_percentile([3], [1], 50, 1)
    test_find_percentile([1, 2, 7, 8, 10], [6, 12],
                         50, 7)
    test_find_percentile([1, 2, 7, 8], [6, 12],
                         50, 6)
    test_find_percentile([15, 20, 35, 40, 50], [],
                         30, 20)
    test_find_percentile([15, 20], [25, 40, 50],
                         40, 20)
    test_find_percentile([15, 20], [25, 40, 50],
                         0, 15)
    test_find_percentile([15, 20], [25, 40, 50],
                         100, 50)
    test_find_percentile([2, 4, 5, 6, 7, 8, 9, 10, 12, 12, 14],
                         [0, 1, 4, 5, 6, 7, 8, 9, 14, 14],
                         50, 7)


def get_random_array(test_size=100, max_value=100):
    return sorted([randint(-max_value, max_value) for i in range(test_size)])


def get_random_test(list1_size, list2_size, max_element_value):
    a, b = [], []
    # at least one list shouldn't be empty
    while not a and not b:
        a = get_random_array(list1_size, max_element_value)
        b = get_random_array(list2_size, max_element_value)
    return a, b


def run_stress_test(min_test_size=0, max_test_size=10, max_attempts=5,
                    max_element_value=1000000):
    print('Stress test started.')
    seed(100)
    for list1_size, list2_size, percentile, attempt in product(
            range(min_test_size, max_test_size + 1),
            range(min_test_size, max_test_size + 1),
            range(101),
            range(max_attempts)):

        if list1_size == list2_size == 0:
            continue

        a, b = get_random_test(list1_size, list2_size, max_element_value)
        correct_answer = reference_solution(a, b, percentile)
        result = find_percentile(a, b, percentile)

        error_str = (f'Stress test failed!\n'
                     f'a: {a}\n'
                     f'b: {b}\n'
                     f'array sizes: {len(a)} and {len(b)}\n'
                     f'percentile: {percentile}\n'
                     f'Result: {result}\n'
                     f'Correct answer: {correct_answer}')
        assert result == correct_answer, error_str

        if percentile == 100 and attempt == max_attempts - 1:
            print(f'Tests for arrays of length {list1_size} '
                  f'and {list2_size} - passed.')
    print('Stress test - SUCCESS')


def run_max_test(max_test_size=150000):
    # generate arrays a and b of maximum possible sizes
    # len(a), len(b) <= 150000 for the problem
    print(f'Max test for arrays of length {max_test_size} started.')
    a, b = get_random_test(max_test_size, max_test_size, 2**31-1)
    percentile = 100
    correct_answer = reference_solution(a, b, percentile)
    t = time()
    result = find_percentile(a, b, 100)
    t = time() - t
    error_str = (f'Stress test failed!\n'
                 f'a: {a}\n'
                 f'b: {b}\n'
                 f'array sizes: {len(a)} and {len(b)}\n'
                 f'percentile: {percentile}\n'
                 f'Result: {result}\n'
                 f'Correct answer: {correct_answer}')
    assert result == correct_answer, error_str
    print(f'Max test - SUCCESS.\nTest time: {t:.4f} sec.')


if __name__ == '__main__':
    run_unit_tests()
    run_stress_test()
    #run_stress_test(min_test_size=14999, max_test_size=15000, max_attempts=10)
    run_max_test()
    run_max_test(1000000)
