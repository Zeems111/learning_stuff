from CountVectorizer import CountVectorizer
import random as rnd


def strgen(number=None, length=None):
    #alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = 'ab'
    alphabet = alphabet.upper()

    if number is None:
        number = rnd.randint(10, 50)
    result = []
    for _ in range(number):
        line = ""
        lng = length
        if length is None:
            lng = rnd.randint(2, 10)
        for _ in range(lng):
            i = rnd.randrange(0, len(alphabet))
            line += alphabet[i]
        result.append(line)
    return result


vect = CountVectorizer(2)
corp = strgen()
print(*corp, sep='\n')

try:
    tr = vect.fit(corp)
except Exception as err:
    print('Error:', err)
print(vect.token_to_index, sep='\n')
try:
    tr = vect.transform(corp)
    print(*tr, sep='\n')
except Exception as err:
    print('Error:', err)
