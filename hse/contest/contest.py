import json


def check_vowels(lines): 
    vowels = 'aeuioy'
    result = []

    for line in lines: 
        count_vowels = set(x for x in line if x in vowels)
        if len(count_vowels) >= 2:
            result.append(line)
    return result


file_name = input()
lines = dict()
with open(file_name, 'r') as f:
    trans = json.load(f)
n = len(trans)
result = {k: [] for k in trans}
for k in range(n):
    lines[str(k + 1)] = input().split('_')
for k, v in trans.items():
    if v == '10':
        result[k].extend(check_vowels(lines[k]))
    elif v == '20':
        result[k].extend([line for line in lines[k] if not len(line) % 2])
    elif v == '30':
        result[k].extend(lines[k])

for k in result:
    result[k].sort(reverse=True)
    
with open('output.json', 'w') as f: 
    json.dump(result, fp=f)