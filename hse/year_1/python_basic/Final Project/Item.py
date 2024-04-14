class Item:
    def __init__(self, name, effect=None, effect_strength=None):
        """Creates an item with a specified name, effect, effect power
        and description"""
        self.name = name
        self.effect = effect
        self.effect_strength = effect_strength

    def __str__(self):
        """Creates a 'string' representation of an item"""
        s = self.name.upper()
        if self.effect and self.effect_strength:
            s += " (" + self.effect
            if self.effect_strength >= 0:
                s += "+" + str(self.effect_strength) + ')'
            else:
                s += '' + str(self.effect_strength) + ')'
        else:
            s += ' (no effect)'
        return s
