'''
data.py

Should contain attacks for various classes, weapon stats, etc.
Mainly just used for potential junk data
'''

# classes = ["knight", "mage", "barbarian"]
classes = ["Knight", "Wizard", "Barbarian"]
difficulties = ["Easy", "Medium", "Hard"]

# Attacks available for each class
# Format: {fast_attack: damage, fast_attack: damage, strong_attack: damage & cooldown}
knight_attacks = {"slash": 3, "low_sweep": 4, "big_swipe": 8}
barbarian_attacks = {"double_hit": 4, "strong_punch": 6, "kick_in_the_balls": 8}
mage_attacks = {"fire_storm": 4, "ice_storm": 4, "magic_rain": 10}


# Attacks for various enemies
dungeon_monster_attacks = {"scratch": 1, "punch": 3, "wait": 0}


