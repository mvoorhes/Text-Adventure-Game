'''
player.py

This file contains the player class
Builds on the monster class by adding various features
'''

import Monsters as ms
import item as wp
import data


class Player(ms.Monster):
    def __init__(self, name, player_class, hp=20):
        
        # Defining player attributes
        self.name = name
        self.player_class = player_class
        self.type = "Player"

        # HP and experience points
        self.max_hp = hp
        self.current_hp = self.max_hp
        self.exp = 0
        self.level = 1

        # Items and attacks
        self.inventory = {}
        self.weapon = wp.Weapon("None", 0)
        self.backpack_limit = 20
        self.attacks = {"wait": 0, "punch": 1}
        self.strong_attacks = {}
        
        self.possible_attacks = {}
        if player_class == "Knight":
            self.possible_attacks = data.knight_attacks
        elif player_class == "Barbarian":
            self.possible_attacks = data.barbarian_attacks
        elif player_class == "Mage":
            self.possible_attacks = data.mage_attacks

        # Currency & other stuff
        self.currency = 0       # can be used at shop vendors

        # 


    # get functions
    def get_class(self):
        return self.player_class
    
    def get_level(self):
        return self.level
    
    def get_exp(self):
        return self.exp
    
    def get_equipped_weapon(self):
        return self.weapon.get_name()
    
    def in_inventory(self, item):
        for thing in self.inventory:
            print(thing.name)
            if thing.name == item:
                return True
        return False
        # return item in self.inventory
    
    def get_currency(self):
        return self.currency
    

    # manipulate functions
    def level_up(self):
        if self.exp % 20 == 0:
            self.level += 1
            self.backpack_limit += 5
        
    def add_item(self, item):
        # self.inventory.append(item)

        if item not in self.inventory:
            self.inventory[item] = 1
        else:
            self.inventory[item] += 1

        # self.inventory[item] += 1
        print("Added", item.name, "to inventory")
        if len(self.inventory) > self.backpack_limit:
            print("You have too many items")
            print(self.inventory)
            while (1):
                print("What do you want to throw out?")
                decision = input()
                if decision in self.inventory:
                    self.drop_item(decision)
                    break
                print("invalid option")

    def drop_item(self, item):
        # Drops all instances of an item
        self.inventory.pop(item)


    def use_item(self, item):

        if item.type == "Potion":
            self.current_hp += item.effect

        self.inventory[item] -= 1
        if self.inventory[item] == 0:
            self.drop_item(item)

    def equip_weapon(self, weapon):
        self.weapon = weapon
        for attack in weapon.attacks:
            self.add_attack(attack)

    def earn_cash(self, cash):
        self.currency += cash


    def win_fight(self):
        self.exp += 5
