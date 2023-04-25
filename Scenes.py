'''
scenes.py

Contains the scenes in this game, including character_creator()
'''

import Monsters as ms
import player as ps
import print_functions as pf
import data
import item as wp
import sys
import time


TEXT_SPEED = 0.02


scene_idled_from = ["Intro", "Mattress", "leave_dungeon"]

global idle_counter


def welcome_message():
    print("Welcome to")
    print(" ________  ___  ___  ________ ")
    print("|        ||   ||   ||  ______|")
    print("|___  ___||   ||   ||  |      ")
    print("   |  |   |   ||   ||  |_____ ")
    print("   |  |   |   ==   ||  ______|")
    print("   |  |   |   ||   ||  |      ")
    print("   |  |   |   ||   ||  |_____ ")
    print("   |__|   |___||___||________|   	text adventure game")
    print("No one has ever made anything like this ever, don't look this up")


def character_creator():
    name = input("Enter name: ")
    p_class = ""
    difficulty = ""
    hp = 30

    print(data.classes)
    while (1):
        p_class = input("Enter class: ")
        if p_class in data.classes:
            break
        print("Invalid Class")


    print(data.difficulties)
    while (1):
        difficulty = input("Select Difficulty: ")
        if difficulty in data.difficulties:
            break
        print("Invalid difficulty")

    if difficulty == "Easy":
        hp = 30
    elif difficulty == "Medium":
        hp = 25
    else:
        hp = 20

    return ps.Player(name, p_class, hp)


def idle(idled):
    if idled == scene_idled_from[0]:
        pf.print_delay("Okay, I guess you're not a very curious person", 1)
        pf.print_delay("...", 1)
        pf.print_delay("...", 1)
        pf.print_delay("...", 1)
        pf.print_delay("I'm not really sure what you expect staring at this wall,", 1)
        pf.print_delay("so we're going to try this again", 1)


def intro_scene(player):
    pf.print_slowly("You are trapped in a locked dungeon cell.", TEXT_SPEED)
    pf.print_slowly("You currently do not have a way to get out of this cell.", TEXT_SPEED)

    options = {1: "Search your surroundings", 2: "Stare at the wall, do nothing"}

    while len(options) > 0:
        pf.print_options(options, TEXT_SPEED)
        decision = int(input())
        if decision == 1:
            search_surroundings(player)
        elif decision == 2:
            idle(scene_idled_from[0])

        options.pop(decision)


def search_surroundings(player):
    pf.print_slowly("You search your surroundings and find a napkin on the floor", TEXT_SPEED)
    pf.print_slowly("There is a message on the napkin that gives you some information", TEXT_SPEED)
    pf.print_slowly(" 'There is a key that will get you out of this cell underneath your bed,", TEXT_SPEED)
    pf.print_slowly(" you should also search under the matress for potential goodies' ", TEXT_SPEED)

    options = {1: "Search under mattress", 2: "Get key from under bed"}

    while len(options) > 0:
        pf.print_options(options, TEXT_SPEED)
        decision = int(input())
        if decision == 1:
            search_mattress(player)
        elif decision == 2 and player.in_inventory("key") == False:
            get_key(player)
            options[decision] = "Leave Dungeon"
            continue
        elif decision == 2 and player.in_inventory("key") == True:

            leave_dungeon(player)

        options.pop(decision)


def search_mattress(player):
    pf.print_slowly("You search under the mattress", TEXT_SPEED)
    weapon = wp.Weapon("Undefined", 0)
    if player.get_class() == data.classes[0]:
        weapon = wp.Sword("Sword", 3)
        pf.print_slowly("Congratulations, you have found a sword", TEXT_SPEED)
    elif player.get_class() == data.classes[1]:
        weapon = wp.Staff("Staff", 3)
        pf.print_slowly("Congratulations, you have found a magic staff", TEXT_SPEED)
    elif player.get_class() == data.classes[2]:
        weapon = wp.Axe("Axe", 3)
        pf.print_slowly("Congratulations, you have found an axe", TEXT_SPEED)

    player.equip_weapon(weapon)


def get_key(player):
    key = wp.Item("key")
    key.write_description("This key will get you out of the dungeon")
    player.add_item(key)
    pf.print_slowly("You now have the key to get out of here", TEXT_SPEED)


def leave_dungeon(player):
    pf.print_slowly("You have now left the dungeon", TEXT_SPEED)
    pf.print_slowly("You walk straight through the door and keep walking until you reach a fork in the road", TEXT_SPEED)

    options = {1: "Go left", 2: "Go right", 3: "Go forward", 4: "?????"}

    while len(options) > 0:
        pf.print_options(options, TEXT_SPEED)
        decision = int(input())
        if decision == 1:
            first_left(player)
        elif decision == 2:
            first_right(player)
        elif decision == 3:
            pf.print_slowly("You go forward and hit the wall so hard that you end up getting a concussion", TEXT_SPEED)
            damage = 7
            player.get_hit(damage)
            message = "You lose" + str(damage) + "health as a result"
            pf.print_slowly(message, TEXT_SPEED)
        elif decision == 4:
            pf.print_slowly("Congratulations, you figured out I meant a literal fork in the road", TEXT_SPEED)
            fork = wp.Item("fork")
            fork.write_description("This fork does nothing helpful, but you can use it to eat food, which I haven't implemented and don't plan to.")
            player.add_item(fork)
        
        options.pop(decision)


def first_left(player):
    pf.print_slowly("You walk for a while and eventually encounter a monster.", TEXT_SPEED)
    pf.print_slowly("It doesn't seem like you can get around it so now you must fight it.", TEXT_SPEED)
    monster = ms.Monster("Monster", 20)
    ms.turn_based_fight(player, monster)
    if player.get_hp()[0] <= 0:
        pf.print_slowly("You have lost the game.", TEXT_SPEED)
        sys.exit(1)

    mystery_door(player)


def first_right(player):
    pf.print_slowly("You walk for a little bit until you reach a dead end.", TEXT_SPEED)
    pf.print_slowly("At this dead end you find that there is a chest.", TEXT_SPEED)

    options = {1: "Open Chest", 2: "Turn around and leave"}

    while len(options) > 0:
        pf.print_options(options, TEXT_SPEED)    

        decision = int(input())
        if decision == 1:
            # Find health potion you can use after you fight the monster
            # On hard difficulty though, this becomes the dark souls mimic chest
            health_potion = wp.Item("Health Potion")
            health_potion.write_description("Heals you to max HP")
            player.add_item(health_potion)
        else:
            # Brings player back to leave_dungeon()
            pf.print_slowly("You go back to where you were", TEXT_SPEED)
        
        options.pop(decision)



def mystery_door(player):
    pf.print_slowly("You have defeated the monster.", TEXT_SPEED)
    pf.print_slowly("Behind this monster is a door.")
    options = {1: "Open door", 2: ""}
    while len(options) > 0:
        pf.print_options(options, TEXT_SPEED)
        decision = int(input())
        if decision == 1:
            return
        elif decision == 2:
            drug_psa()


def drug_psa():
    pf.print_slowly("The item you just used was actually laced with marijuana. You died as a result", TEXT_SPEED)
    pf.print_slowly("Remember, it's never cool to do drugs under any circumstance.", TEXT_SPEED)
    pf.print_slowly("You will die.", TEXT_SPEED)
    sys.exit(1)