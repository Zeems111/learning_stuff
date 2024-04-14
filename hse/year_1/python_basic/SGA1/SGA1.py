def typecast(number, new_type):
    try:
        number = new_type(number)
    except ValueError:
        number = None
    return number


def grade(offer):
    offer_grade = 'other'
    if offer['price'] < 200 and offer['transfers'] <= 1 and offer['refund'] and offer['luggage']:
        offer_grade = 'the best'
    elif 200 <= offer['price'] <= 250 and offer['transfers'] <= 2:
        offer_grade = 'good enough'
    elif offer['price'] > 250 and offer['transfers'] >= 3:
        offer_grade = 'the worst'
    return offer_grade


def my_grade(offer, priority):
    std_offer = {'price': 700, 'transfers': 2, 'duration': 16,
                 'comfort': 2, 'refund': True, 'luggage': True}
    mygrade = {}

    if offer['price'] <= 0.85 * std_offer['price']:
        mygrade['price'] = 5
    elif offer['price'] <= 0.95 * std_offer['price']:
        mygrade['price'] = 4
    elif offer['price'] <= 1.05 * std_offer['price']:
        mygrade['price'] = 3
    elif offer['price'] <= 1.15 * std_offer['price']:
        mygrade['price'] = 2
    else:
        mygrade['price'] = 1

    if offer['transfers'] < std_offer['transfers']:
        mygrade['transfers'] = 5
    elif offer['transfers'] == std_offer['transfers']:
        mygrade['transfers'] = 3
    else:
        mygrade['transfers'] = 1

    if offer['duration'] <= 0.85 * std_offer['duration']:
        mygrade['duration'] = 5
    elif offer['duration'] <= 0.95 * std_offer['duration']:
        mygrade['duration'] = 4
    elif offer['duration'] <= 1.05 * std_offer['duration']:
        mygrade['duration'] = 3
    elif offer['duration'] <= 1.15 * std_offer['duration']:
        mygrade['duration'] = 2
    else:
        mygrade['duration'] = 1

    if offer['comfort'] < std_offer['comfort']:
        mygrade['comfort'] = 1
    elif offer['comfort'] == std_offer['comfort']:
        mygrade['comfort'] = 3
    else:
        mygrade['comfort'] = 5

    if offer['refund']:
        mygrade['refund'] = 5
    else:
        mygrade['refund'] = 1

    if offer['luggage']:
        mygrade['luggage'] = 5
    else:
        mygrade['luggage'] = 1

    for k in offer.keys():
        mygrade[k] = mygrade[k] * priority[k]

    return mygrade


print('Welcome to flight tickets evaluation!')
# newOffer = {'price': 580, 'transfers': 1, 'duration': 15,
#            'comfort': 3, 'refund': False, 'luggage': False}

newOffer = {'price': None, 'transfers': None, 'duration': None,
            'comfort': None, 'refund': None, 'luggage': None}

while newOffer['price'] is None:
    price = input('[>] Enter ticket price: $')
    price = typecast(price, float)
    if price is None or price < 0:
        print('[X] Incorrect input')
        continue
    newOffer['price'] = round(price, 2)

while newOffer['transfers'] is None:
    transferNumber = input('[>] Number of transfers: ')
    transferNumber = typecast(transferNumber, int)
    if transferNumber is None or transferNumber < 0:
        print('[X] Incorrect input')
        continue
    newOffer['transfers'] = transferNumber

while newOffer['duration'] is None:
    duration = input('[>] Enter flight duration (hours): ')
    duration = typecast(duration, float)
    if duration is None or duration <= 0:
        print('[X] Incorrect input')
        continue
    newOffer['duration'] = round(duration, 1)

comfortlevel = ['First class', 'Business class', 'Economy']
while newOffer['comfort'] is None:
    print('Enter a number, which corresponds to ticket\'s comfort level')
    print(*(str(i+1) + '. ' + comfortlevel[i] for i in range(len(comfortlevel))), sep='\n')
    comfort = input('[>] Comfort level: ')
    comfort = typecast(comfort, int)
    if comfort is None or not 1 <= comfort <= 3:
        print('[X] Incorrect input')
        continue
    newOffer['comfort'] = 7 - 2 * comfort

while newOffer['refund'] is None:
    refund = input('[>] Is refund included (Y/N)?: ').lower()
    if refund != 'y' and refund != 'n':
        print('[X] Incorrect input')
        continue
    newOffer['refund'] = refund == 'y'

while newOffer['luggage'] is None:
    luggage = input('[>] Is luggage cost included (Y/N)?: ').lower()
    if luggage != 'y' and luggage != 'n':
        print('[X] Incorrect input')
        continue
    newOffer['luggage'] = luggage == 'y'

priorities = {'comfort': 1, 'price': 1, 'transfers': 1,
              'luggage': 1, 'refund': 1, 'duration': 1}

# print('Set priorities (from 0 - \"doesn\'t matter\" to 5 - \"most important\")')

priorList = list(priorities.keys())
prior = None
print('Select main priority from the list below')


for i in range(len(priorList)):
    print(i + 1, priorList[i])
while prior is None:
    prior = input('[>] Main priority number: ')
    prior = typecast(prior, int)
    if prior is None or prior <= 0 or prior > len(priorList):
        print('[X] Incorrect input')
        prior = None
        continue
    priorities[priorList[prior-1]] = 4

prior = None
print('Select second priority from the list below')
print('0 No second priority')
for i in range(len(priorList)):
    print(i + 1, priorList[i])

while prior is None:
    prior = input('[>] Second priority number: ')
    if prior == '0':
        break
    prior = typecast(prior, int)
    if prior is None or prior <= 0 or prior > len(priorList):
        print('[X] Incorrect input')
        prior = None
        continue
    priorities[priorList[prior-1]] = 2

n = sum(priorities.values())
for key in priorities.keys():
    priorities[key] = priorities[key]/n
print(priorities)

print()
print('--- FLIGHT INFORMATION ---')
print('Ticket price: $', newOffer['price'], sep='')
print('Number of transfers:', newOffer['transfers'])
print('Flight duration: ', newOffer['duration'], 'hours', sep='')
comfi = (5 - newOffer['comfort']) // 2
print('Comfort level:', comfortlevel[comfi])
refInclusion = '' if newOffer['refund'] else 'not '
print('Refund: ', refInclusion, 'included', sep='')
luggageInc = '' if newOffer['luggage'] else 'not '
print('Luggage: ', luggageInc, 'included', sep='')

finalGrade = my_grade(newOffer, priorities)
rating = round(sum(finalGrade.values()), 2)
print('Offer rating: ', rating, sep='')
