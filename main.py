'''
main.py

The main program. To run using python3
python3 main.py
'''


import Monsters as ms
import player as ps
import Scenes as sc


sc.welcome_message()

main_character = sc.character_creator()

sc.intro_scene(main_character)