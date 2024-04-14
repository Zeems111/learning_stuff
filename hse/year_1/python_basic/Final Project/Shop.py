class Shop:
    def __init__(self, items):
        """Creates a shop with a dictionary, which consists of
         pairs {item: quantity}"""
        self.inventory = items

    def __str__(self):
        """Creates a 'string' representation of a shop"""
        s = '\n'.join(item.name + ' ($' + str(self.inventory[item]) + ')'
                      for item in self.inventory)
        return s
