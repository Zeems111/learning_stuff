res = {*range(1, int(input()) + 1)}
print(res)

while True:
    s = input()
    if s == 'HELP':
        break
    lst = {*map(int, s.split())}
    print(lst)
    s = input()
    if s == 'YES':
        res &= lst
        print(res)
    if s == 'NO':
        res -= lst
        print(res)

print(*sorted(res))