class Enemy:
    def __init__(self, name, level, completion=100):
        """Creates an enemy, like a 'quiz', with specified name,
        difficulty level and 'health' - completion level.
        'To kill an enemy' is 'to complete a task'.
        If completion is equal to 0, task is considered completed"""
        self.name = name
        self.level = level
        self.completion = completion
        self.current_completion = completion

    def attack(self, char):
        """Calculates damage done to character with relation
        to difficulty level"""
        dmg = 3 * self.level
        return char.get_damage(dmg)

    def set_completion(self, damage):
        """Applies damage received from hero's attacks"""
        received_dmg = damage // self.level
        received_dmg = min(received_dmg, self.current_completion)
        self.current_completion -= received_dmg
        return received_dmg
