import html
import html.parser
from bs4 import BeautifulSoup
text = ''
with open('c:/learning_stuff/hse/year_1/data_scrapping/week4/index.html', 'r', encoding='utf8') as f:
    for line in f:
        text += line
tree = BeautifulSoup(text, 'html.parser')
tags = set(tag.name for tag in tree.findAll())
print(tags)
print(len(tags))
    

