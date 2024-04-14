import sys
from IPython.display import clear_output
from Character import Character
from Enemy import Enemy
from Item import Item
from Shop import Shop


def typecast(number, new_type):
    """Converts 'number' to a 'new_type'
    (i.e. int or float), otherwise returns None"""
    try:
        number = new_type(number)
    except ValueError:
        number = None
    return number


def menu_activity(char, act):
    """Selects an action from 'game' menu, which are represented by other
    functions defined inside it"""
    def menu_toggle():
        """Sends user to game menu or back into the game"""
        global location, time_h
        time_h -= 1
        if location == 'Menu':
            location = char.location
        else:
            location = 'Menu'

    def show_info():
        """Displays game information and hero's description"""
        global difficulty, time_h
        time_h -= 1
        diffs = ['Easy', 'Normal', 'Hard', 'HSE']
        print('Difficulty:', diffs[difficulty-1])
        print(char)

    def set_difficulty():
        """Sets game difficulty level and updates in-game objects'
        characteristics according to it.\n
        1 - Easy\n
        2 - Normal\n
        3 - Hard\n
        4 - HSE\n
        """
        global difficulty, time_h, boss
        time_h -= 1
        boss.level -= difficulty
        boss.completion //= difficulty
        boss.current_completion //= difficulty
        i = None
        while i is None:
            i = input("Select difficulty (1 - easy, 2 - normal, "
                      "3 - hard, 4 - HSE): ")
            i = typecast(i, int)
            if i is None or i < 1 or i > 4:
                print('[X] Incorrect input')
                i = None
                continue
            difficulty = i
        boss.level += difficulty
        boss.completion *= difficulty
        boss.current_completion *= difficulty

    def alwaysshowheroinfo():
        """Toggles hero's information display On|Off"""
        global always_show_info, time_h
        always_show_info = not always_show_info
        time_h -= 1

    def quit_game():
        """Allows to exit the game without completing it"""
        print('You quited the game')
        sys.exit(0)

    ma = {'To the game': menu_toggle,
          'Show game info': show_info,
          'Always show hero info': alwaysshowheroinfo,
          'Select difficulty': set_difficulty,
          'Quit': quit_game}
    ma[act]()


def home_activity(char, act):
    """Selects an action from 'Home' menu, which are represented by other
        functions defined inside it"""
    def rest():
        """Restores hero's energy by 15"""
        global time_h
        energy_cost = 15
        if char.attributes['Energy'] == char.attributes['Stamina']:
            print('You are full of energy!')
            time_h -= 1
        char.change_energy(energy_cost)

    def workout():
        """Permanently increases hero's stamina, which allows
        hero to do more actions later on and also makes his
        actions more effective"""
        energy_cost = 10
        char.change_energy(-energy_cost)
        char.attributes['Stamina'] += 4 // difficulty
        print(f"Your Stamina increased by {4 // difficulty}!")

    def study():
        """Permanently increases hero's intellect, which allows
        hero to complete tasks with less effort"""
        energy_cost = 10
        energy = char.attributes['Energy']
        stam = char.attributes['Stamina']
        productivity = energy / stam
        if difficulty > 0:
            productivity /= difficulty
        char.attributes['Smarts'] += int(10 * productivity)
        char.change_energy(-energy_cost)

    def use_item():
        """Makes hero consume an item and applies its effect to hero"""
        energy_cost = 0
        global time_h
        if not char.myitems:
            time_h -= 1
            print('You have no items to use')
            return

        itemslist = list(char.myitems.keys())
        i = None
        while i is None:
            for i in range(len(itemslist)):
                print(i + 1, itemslist[i], ' (' +
                      str(char.myitems[itemslist[i]]) + ')')

            i = input('Select an item to use (enter it\'s number): ')
            i = typecast(i, int)
            i -= 1
            if i is None or i < 0 or i >= len(itemslist):
                print('[X] Incorrect input')
                i = None
                continue
            i = itemslist[i]
        char.use(i)
        time_h -= 1
        char.change_energy(-energy_cost)

    def quiz_fight():
        """Simulates a 'fight' - process of task completion.\n
        Consumes hero's energy according to his mental
        capacity and game difficulty"""
        global difficulty, quiz_count, time_h
        if quiz_count == 0:
            print('There are no quizzes left for today')
            time_h -= 1
            return

        quiz_count -= 1
        quiz = Enemy('Casual Assignment',
                     0, 100 + 50 * difficulty)
        quiz.level += difficulty

        cmpl = quiz.completion
        print(char.name, quiz.name, sep='\t\t')
        print(f"Energy: {char.attributes['Energy']}\t\t"
              f"{quiz.name} completion: {quiz.current_completion}")
        while char.attributes['Energy'] > 0 and quiz.current_completion > 0:
            hd = char.attack(quiz)
            print(f"You've completed task by {round(hd/cmpl*100,2)}%")
            bd = quiz.attack(char)
            print(f"Your energy was depleted by {bd}")
            print(f"Energy: {char.attributes['Energy']}\t\t"
                  f"{quiz.name} completion: {quiz.current_completion}")

        if quiz.current_completion == 0:
            energy = char.attributes['Energy']
            stam = char.attributes['Stamina']
            productivity = energy / stam
            productivity /= difficulty
            char.attributes['Smarts'] += int(20 * productivity)

    def final_boss():
        """Simulates a 'fight with a boss - final project'\n
        Consumes hero's energy according to his mental
        capacity and game difficulty"""
        global boss
        print(char.name, boss.name, sep='\t\t')
        print(f"Energy: {char.attributes['Energy']}\t\t\t"
              f"{boss.name} completion:{boss.completion}")

        cmpl = boss.completion
        while char.attributes['Energy'] > 0 and boss.current_completion > 0:
            hd = char.attack(boss)
            print(f"You've completed task by {round(hd/cmpl*100,2)}%")
            bd = boss.attack(char)
            print(f"Your energy was depleted by {bd}")
            print(f"Energy: {char.attributes['Energy']}\t\t"
                  f"{boss.name} completion:{boss.current_completion}")

        if boss.current_completion == 0:
            print("VICTORY!")
            print("You've completed the Final Project!")
            print("Great job!")
            sys.exit()

    def go_work():
        """Allows hero to travel to work from home in the morning"""
        energy_cost = 10
        global time_h, location
        if time_h > 16:
            time_h -= 1
            print('You are tired enough, '
                  'there is no way you are going back')
            return
        char.change_energy(-energy_cost)
        char.location = 'Work'
        location = char.location

    ha = {'Use an item': use_item,
          'Rest': rest, 'Work out': workout,
          'Study': study,
          'Take a quiz': quiz_fight,
          'Work on the final project': final_boss,
          'Go to work': go_work}

    global time_h
    if time_h == 8 and act != 'Go to work':
        print("You don't have enough time, you have to go to work...")
        time_h -= 1
        return
    ha[act]()


def work_activity(char, act):
    """Selects an action from 'Work' menu, which are represented by other
    functions defined inside it"""

    def work_closed():
        """Checks if working facilities are open"""
        global difficulty, time_h
        closing_time = 24 - difficulty
        return time_h >= closing_time

    def do_work():
        """Allows hero to suffer at work in exchange for some money"""
        energy_cost = 20
        global time_h, day, difficulty
        time_h += 4
        char.change_energy(-energy_cost)
        char.money += 100 // difficulty
        print(f"You earned another ${100 // difficulty}")
        if work_closed():
            print("You got extremely tired while working too hard")
            print("When everyone were leaving noone "
                  "noticed you lying on the floor")
            print("You got locked in the facilities "
                  "and had to cry here the whole night")
            time_h = 24
        time_h -= 1

    def waste_time():
        """Allows hero to have some rest at work while losing
        a chance to get money"""
        global time_h, day, difficulty
        i = None
        while i is None:
            i = input(f'How much time do you want to spend '
                      f'(0-{24-time_h}): ')
            i = typecast(i, int)
            if i is None or i < 0 or i > 24 - time_h:
                print('[X] Incorrect input')
                i = None
                continue
        time_h += i
        char.change_energy(2 * i)
        if work_closed():
            print("You got tired while wasting all that time and fell asleep")
            print("When everyone were leaving noone noticed you")
            print("You got locked in the facilities and have to sleep here")
            time_h = 24
        time_h -= 1

    def go_home():
        """Allows hero to travel back home from work"""
        energy_cost = 10
        global time_h, location
        if time_h < 16:
            print('You can\'t leave yet')
            time_h -= 1
            return
        char.change_energy(-energy_cost)
        char.location = 'Home'
        location = char.location

    def go_shop():
        """Allows hero to travel to shop from work"""
        energy_cost = 5
        global time_h, location
        if time_h < 16:
            print('You still have some work to do')
            time_h -= 1
            return
        char.change_energy(-energy_cost)
        location = 'Shop'

    wa = {'Suffer': do_work,
          'Waste some time': waste_time,
          'Go home': go_home,
          'Go to shop': go_shop}
    wa[act]()


def shop_activity(char, act):
    """Selects an action from 'Shop' menu, which are represented by other
        functions defined inside it"""
    def buy_item():
        """Allows hero to pick an item from shop in exchange for some money"""
        global shop, time_h
        time_h -= 1
        shoplist = list(name for name in shop.inventory.keys()
                        if shop.inventory[name] < char.money)
        if len(shoplist) == 0:
            print("You don't have enough money!")
            return

        i = None
        while i is None:
            for i in range(len(shoplist)):
                print(i + 1, shoplist[i], '\t$' +
                      str(shop.inventory[shoplist[i]]))

            i = input('Select an item to buy (enter it\'s number): ')
            i = typecast(i, int)
            if i is None or i < 1 or i > len(shoplist):
                print('[X] Incorrect input')
                i = None
                continue
            i -= 1
            i = shoplist[i]
        if i in char.myitems.keys():
            char.myitems[i] += 1
        else:
            char.myitems[i] = 1
        char.money -= shop.inventory[i]

    def go_home():
        """Allows hero to travel home from shop"""
        energy_cost = 5
        global location
        char.location = 'Home'
        location = char.location
        char.change_energy(-energy_cost)

    sa = {'Buy an item': buy_item,
          'Go home': go_home}
    sa[act]()


def select_activity(char):
    """Contains lists of actions for each location and allows to select
    actions corresponding to hero's current location"""
    global location, time_h
    menu_activities = ['Show game info', 'Always show hero info',
                       'Select difficulty', 'Quit']
    home_activities = ['Use an item', 'Rest', 'Work out',
                       'Study', 'Take a quiz',
                       'Work on the final project',
                       'Go to work']
    work_activities = ['Suffer', 'Waste some time',
                       'Go home', 'Go to shop']
    shop_activities = ['Buy an item', 'Go home']
    activities_at = {'Menu': menu_activities,
                     'Home': home_activities,
                     'Work': work_activities,
                     'Shop': shop_activities,
                     }

    act = None
    while act is None:
        print("What are you going to do next?")
        if location == 'Menu':
            print(0, 'To the game')
        elif location != 'Menu':
            print(0, 'Menu')

        for i in range(len(activities_at[location])):
            print(i + 1, activities_at[location][i])

        act = input('Select an option (enter it\'s number): ')
        clear_output()
        act = typecast(act, int)
        if act is None or act > len(activities_at[location]) or act < 0:
            print('[X] Incorrect input')
            act = None
            continue

    act -= 1
    if act == -1:
        if location == 'Menu':
            location = char.location
        else:
            location = 'Menu'
        time_h -= 1
        return 0

    act = activities_at[location][act]
    if location == 'Menu':
        menu_activity(char, act)
        return 0
    if location == 'Home':
        home_activity(char, act)
        return 0
    if location == 'Work':
        work_activity(char, act)
        return 0
    if location == 'Shop':
        shop_activity(char, act)
        return 0


def create_hero():
    """Allows user to create a character with specified name and
    parameters"""
    total = 100
    stats = {'Energy': None, 'Stamina': None, "Smarts": None}

    print("It's time to create your character!")
    name = input("Type in your character's name: ")
    print("You have 100 points in total.\nDistribute them well!")

    val = None
    while val is None:
        val = input(f'Stamina (0 - {total}): ')
        val = typecast(val, int)
        if val is None or val < 0 or val > total:
            print('[X] Incorrect input')
            val = None
            continue

    stats['Stamina'] = val
    stats['Energy'] = stats['Stamina']
    total -= val

    val = None
    while val is None:
        val = input(f'Smarts (0 - {total}): ')
        val = typecast(val, int)
        if val is None or val < 0 or val > total:
            print('[X] Incorrect input')
            val = None
            continue

    stats['Smarts'] = val
    return Character(name, stats)


# shop items
apple = Item("apple", "Energy", 2)
coffee1 = Item("Espresso", "Energy", 5)
coffee2 = Item("Double Espresso", "Energy", 10)
nrj_drink = Item("Energy drink", "Energy", 15)
inventory = {apple: 20, coffee1: 50, coffee2: 90, nrj_drink: 130}
shop = Shop(inventory)

# General game setting
difficulty = 2
location = 'Menu'
quiz_count = 3
day = 1
time_h = 7
always_show_info = False

hero = create_hero()
boss = Enemy('Final Project', 2 + difficulty, 1250 * difficulty)

while day <= 7:
    print()
    print(f'Location: {location}\t\t\t\t\t\tDAY {day:02} ({time_h:02}:00)')
    if always_show_info:
        print('\t\t\t\tHero', hero, sep=' ')
    print()

    try:
        select_activity(hero)
    except SystemExit:
        break
    time_h += 1

    if hero.attributes['Energy'] <= 0 or time_h >= 24:
        if location == 'Home':
            print('Tired to death you went to sleep')
        elif location == 'Work' and hero.attributes['Energy'] <= 0:
            print('Tired to death you fell to the floor right at work')
            print('You were brought back home by your friend coworker')
            location = 'Home'
        elif location == 'Shop':
            print('Tired to death you fell asleep right in the shop')
            print('You were brought back home by ambulance')
            location = 'Home'
        time_h = 7
        day += 1
        hero.location = location
        hero.attributes['Energy'] = hero.attributes['Stamina']
        quiz_count = 3
else:
    print("\tGAME OVER")
    print('YOU FAILED THE DEADLINE')
