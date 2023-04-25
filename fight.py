'''
fight.py

Defines fight code between two characters
'''

import Monsters as ms


def turn_based_fight(monster1, monster2):
    # Turn: True = monster1; False = monster2
    turn = True

    _round_ = 0
    _winner_ = ''

    move = ''
    damage = 0

    while monster1.current_hp > 0 and monster2.current_hp > 0:

        _round_ += 1

        if turn == True:
            current_player = monster1
            opposing_player = monster2
        else:
            current_player = monster2
            opposing_player = monster1

        print(current_player.name, "Turn")

        move, damage = current_player.get_move()
        opposing_player.get_hit(damage)

        print(current_player.name, "used", move, "and caused", damage, "damage to", opposing_player.name)

        print(monster1.current_hp)
        print(monster2.current_hp)
        turn = ~turn

    if monster1.current_hp <= 0 and monster2.current_hp > 0:
        _winner_ = monster2
    elif monster2.current_hp <= 0 and monster1.current_hp > 0:
        _winner_ = monster1


    return _round_, _winner_