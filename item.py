'''
item.py

defines item and weapon classes
'''


class Item:
    def __init__(self, name):
        self.name = name
        self.type = "Misc"
        self.description = ""

    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def write_description(self, message):
        self.description = message


class Potion(Item):
    def __init__(self, name, effect, points):
        super().__init__(name)
        self.type = "Potion"
        self.effect = effect
        self.points = points


class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage        # damage multiplier
        self.attacks = {}
        self.description = ""

    def get_name(self):
        return self.name
    
    def get_attacks(self):
        return self.attacks
    
    def get_description(self):
        return self.description
    
    def get_attacks(self):
        return self.attacks
    
    def write_description(self, message):
        self.description = message
    

class Sword(Weapon):
    def __init__(self, name, damage):
        super().__init__(name, damage)
        self.attacks = {"slash": 3, "low_sweep": 3, "big_swipe": 8}


class Staff(Weapon):
    def __init__(self, name, damage):
        super().__init__(name, damage)
        self.attacks = {"fire_storm": 4, "ice_storm": 4, "magic_rain": 10}


class Axe(Weapon):
    def __init__(self, name, damage):
        super().__init__(name, damage)
        self.attacks = {"double_hit": 4, "strong_punch": 6, "kick_in_the_balls": 8}


class Dagger(Weapon):
    def __init__(self, name, damage):
        super().__init__(name, damage)
        self.attacks = {"slice": 1, "stab": 2}