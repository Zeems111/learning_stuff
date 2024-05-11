import math
'''
10
2
10 9 8 7 6 5 4 3 2 1
'''
def binary_pos(array, elem, left, right):
    if left == right:
        if array[left] > elem:
            return left
        else:
            return left + 1
        
    if left > right:
            return left
    
    mid = (left + right) // 2
    if array[mid] < elem:
        return binary_pos(array, elem, mid + 1, right)
    elif array[mid] > elem:
        return binary_pos(array, elem, left, mid - 1)
    else:
        return mid
     
def find_percentile(array, percentage):
    last = array[-1]
    arr = array[:-1]
    k = math.ceil(percentage / 100 * len(arr))
    pos = binary_pos(arr, last, 0, len(arr)-1)    
    arr.insert(pos, last)
    array = arr
    if last > arr[k-1]:
          return array, last
    else:
          return array, -1

M = int(input())
K = int(input())
numbs = [int(x) for x in input().split()]
left = sorted(numbs[:K])
right = numbs[K:]
numbs = left + right
if M != K:
    K -= 1 
    perc = -1
    for day in range(K + 1, M):
        slice = numbs[:day+1]
        slice, perc = find_percentile(slice, 90)
        numbs = slice + numbs[day+1:]
        #print(numbs)
        if perc != -1:
            print(day+1)
            break
    if perc == -1:
         print(-1)
else:
     print(-1)