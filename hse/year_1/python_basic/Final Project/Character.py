class Character:
    def __init__(self, name, attributes):
        """Creates the main character of the game
        with specified name and basic stats, determined by
        'attributes' dictionary.
        Starting location: at home.
        Money: $50."""
        self.name = name
        self.attributes = attributes
        self.location = 'Home'
        self.money = 50
        self.myitems = {}

    def __str__(self):
        """Creates a 'string' representation of a character"""
        s = "\x1B[1m" + self.name.upper() + "\x1B[0m\n"
        s += '\n'.join(f"{attr}\t\t{value}"
                       for attr, value in self.attributes.items())
        s += "\nMoney\t\t$" + str(self.money) + '\n'
        s += "Your items:\n"
        s += '\n'.join(f"{item}({price})" for item, price in self.myitems.items())
        if not self.myitems:
            s += 'none'
        return s

    def change_energy(self, value):
        """Changes 'Energy' stat by 'value' in such a way, that
        0 <= Energy <= Stamina"""
        self.attributes['Energy'] += value
        if self.attributes['Energy'] < 0:
            self.attributes['Energy'] = 0
        elif self.attributes['Energy'] > self.attributes['Stamina']:
            self.attributes['Energy'] = self.attributes['Stamina']

    def get_damage(self, damage):
        """Applies damage dealt by other entities with consideration
        of game difficulty and hero's characteristics,
        i.e. smarter hero gets tired less from studying"""
        damage = damage * (100 - self.attributes['Smarts']) / 100
        received_dmg = int(round(damage, 0))
        received_dmg = min(received_dmg, self.attributes['Energy'])
        self.attributes['Energy'] -= received_dmg
        return received_dmg

    def attack(self, enemy):
        """Calculates 'damage' dealt to enemies with consideration of
        hero's mental capacity and how tired he is at the moment"""
        mind_power = self.attributes['Energy'] / 100
        dmg = int(10 * self.attributes['Smarts'] * mind_power)
        return enemy.set_completion(dmg)

    def use(self, item):
        """Consumes an item and applies its effect to hero"""
        if item not in self.myitems.keys():
            return
        print(self.name, 'used an item:', item)
        self.myitems[item] -= 1
        if self.myitems[item] == 0:
            del self.myitems[item]
        if item.effect:
            self.attributes[item.effect] += item.effect_strength
        return
