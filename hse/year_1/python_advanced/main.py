import re

all = []
regexp = re.compile(r'<i>(.*?)</i>')
#for line in sys.stdin:
# with open("words.txt") as f:
    for line in f:
        text_match = regexp.findall(line)
        if text_match:
            all.extend(text_match)
print(*all,sep='\n')