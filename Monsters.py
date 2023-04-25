from itertools import cycle
import AI
import data


class Monster:
    def __init__(self, name, hp=20):
        self.name = name
        self.type = "Enemy"
        self.max_hp = hp
        self.current_hp = self.max_hp
        self.exp = 0
        self.attacks = data.dungeon_monster_attacks
        self.possible_attacks = data.dungeon_monster_attacks

    # Accessor functions
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_hp(self):
        return self.max_hp, self.current_hp

    def get_attacks(self):
        for attack in self.attacks:
            print(attack)


    # Male Manipulator functions

    def add_attack(self, attack_name):
        if attack_name in self.attacks:
            # if attack already exists, closes function
            return False
        elif attack_name in self.possible_attacks:
            if len(self.attacks) == 4:
                # removes lowest attack if there are 4 attacks
                sorted_attacks = []
                for x in self.attacks:  # creates list of tuples
                    sorted_attacks.append((self.attacks[x], x))
                sorted_attacks = sorted(sorted_attacks)
                del sorted_attacks[0]
                self.attacks = {}
                for i in sorted_attacks:  # adds attacks back into list
                    self.attacks[i[1]] = i[0]
            self.attacks[attack_name] = self.possible_attacks[attack_name]
            return True
        else:
            return False

    def remove_attack(self, attack_name):
        if attack_name in self.attacks:
            del self.attacks[attack_name]
            if self.attacks == {}:  # if list is empty, adds wait
                self.attacks["wait"] = self.possible_attacks["wait"]
            return True
        else:
            return False

    def win_fight(self):
        self.exp += 5

    def lose_fight(self):
        self.exp += 1

    def get_hit(self, damage):
        self.current_hp -= damage

    def get_move(self):
        move = ''
        damage = 0
        
        if self.get_type() == "Player":
            self.get_attacks()
            while (1):
                move = input("Enter Move: ")
                if move not in self.attacks:
                    print("invalid move")
                    continue
                damage = self.attacks.get(move)
                break
        elif self.get_type() == "Enemy":
            # Placeholder code until I get AI to work
            damage = max(self.attacks.values())
            move = max(self.attacks, key=self.attacks.get)

            # successor_states = AI.get_successor_states()
        
        return move, damage


    def max_to_min_attack(self):
        values = self.attacks.values()
        keys = self.attacks.keys()
        attacks = self.attacks.items()
        values = sorted(values, reverse=True)
        keys = sorted(keys)
        attacks = sorted(attacks)
        sorted_attacks = []
        end = len(attacks) - 1

        for x, y, z, r in zip(values, keys, attacks, range(len(attacks))):
            if x != z[1]:
                if x > end:
                    y = attacks[r+1][0]
                else:
                    y = attacks[r-1][0]
            sorted_attacks.append((y, x))


        self.attacks = {}
        for i in sorted_attacks:  # adds attacks back into list
            self.attacks[i[0]] = i[1]

    def min_to_max_attack(self):
        sorted_attacks = []
        for x in self.attacks:  # creates list of tuples
            sorted_attacks.append((self.attacks[x], x))
        sorted_attacks = sorted(sorted_attacks)
        self.attacks = {}
        for i in sorted_attacks:  # adds attacks back into list
            self.attacks[i[1]] = i[0]


class Ghost(Monster):
    def win_fight(self):
        before = self.exp
        Monster.win_fight(self)
        after = self.exp
        self.level_up(before, after)
        self.current_hp = self.max_hp

    def lose_fight(self):
        before = self.exp
        Monster.lose_fight(self)
        after = self.exp
        self.level_up(before, after)
        self.current_hp = self.max_hp

    def level_up(self, before, after):
        if after % 10 == 0 or after % 10 < before % 10:
            self.max_hp += 5


class Dragon(Monster):
    def win_fight(self):
        before = self.exp
        Monster.win_fight(self)
        after = self.exp
        self.level_up(before, after)

    def lose_fight(self):
        before = self.exp
        Monster.lose_fight(self)
        after = self.exp
        self.level_up(before, after)

    def level_up(self, before, after):
        if (after % 10 == 0 or after % 10 < before % 10):
            for i in self.attacks:
                self.attacks[i] += 1



# Fight functions

# Automated monster fight: player can choose this if they don't want to bother playing the game
def monster_fight(monster1, monster2):

    _round_ = 0
    _winner_ = ''
    _moves_ = []
    moves1 = []
    moves2 = []

    monster1.max_to_min_attack()
    monster2.max_to_min_attack()

    for i, j in zip(cycle(monster1.attacks), cycle(monster2.attacks)):

        _round_ += 1

        if monster1.attacks == {"wait": 0} and monster2.attacks == {"wait": 0}:
            return -1, None, None

        monster2.current_hp -= monster1.attacks[i]
        monster1.current_hp -= monster2.attacks[j]
        moves1.append(i)
        moves2.append(j)

        if monster2.current_hp <= 0:
            _winner_ = monster1
            _moves_ = moves1
            monster1.win_fight()
            monster2.lose_fight()
            monster1.min_to_max_attack()
            monster2.min_to_max_attack()
            break
        if monster1.current_hp <= 0:
            _winner_ = monster2
            _moves_ = moves2
            monster2.win_fight()
            monster1.lose_fight()
            monster1.min_to_max_attack()
            monster2.min_to_max_attack()
            break

    return _round_, _winner_, _moves_


# Turn based fight
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