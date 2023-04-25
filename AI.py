import Monsters as ms
import numpy as np
import copy


global alpha
global beta

PLAYER1 = 0
PLAYER2 = 1


def get_successor_states(player1, player2, turn):
    """
    Gets next possible states given two players

    player1: current player (the AI we are programming)
    player2: opponent player
    turn: whose turn is it?
        True: player1
        False: player2
    """

    successor_states = []

    if turn:
        current_player = player1
        opponent = player2
    else:
        current_player = player2
        opponent = player1

    for attack in current_player.attacks.values():
        opponent_copy = copy.deepcopy(opponent)
        opponent_copy.current_hp -= attack
        current_copy = copy.deepcopy(current_player)

        # next state = (player1, player2)
        if turn:
            next_state = (current_copy, opponent_copy)
        else:
            next_state = (opponent_copy, current_copy)

        successor_states.append(next_state)

    return successor_states


def evaluation_function(player1, player2):
    if player1.current_hp <= 0 and player2.current_hp > 0:
        return -100 # AI has lost
    elif player1.current_hp > 0 and player2.current_hp <= 0:
        return 100  # AI has won
    elif player1.current_hp == player2.current_hp:
        return 0    # Currently a tie
    
    utility = player1.current_hp - player2.current_hp

    return utility


# Value(state) function for AB pruning
# turn: next agent
#   true: player1s turn; max-value
#   false: player2s turn; min-value
def value(player1, player2, turn, depth, alpha, beta):
    utility = evaluation_function(player1, player2)
    if utility == 100 or utility == -100 or depth == 5:
        return utility
    elif turn:
        return max_value(player1, player2, turn, depth, alpha, beta)
    else:
        return min_value(player1, player2, turn, depth, alpha, beta)
    

def max_value(player1, player2, turn, depth, alpha, beta):
    v = -np.inf
    successor_states = get_successor_states(player1, player2, turn)
    for state in successor_states:
        v = max(v, value(state[PLAYER1], state[PLAYER2], ~turn, depth + 1, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(player1, player2, turn, depth, alpha, beta):
    v = np.inf
    successor_states = get_successor_states(player1, player2, turn)
    for state in successor_states:
        v = min(v, value(state[PLAYER1], state[PLAYER2], ~turn, depth + 1, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


# Plans: Implement alpha beta pruning


# Pseudocode
# get-move
#   move = ''
#   damage = 0
#   getSuccessorStates(player1, player2)
#   for state in successor states
#       temp = value()
#       if temp > max
#           max = temp
#   return max

# value(player1, player2, depth, alpha, beta)
#   utility = evaluation_function(player1, player2)
#   if terminal state
#       return utility
#   else if next agent is MAX
#       return max-value(player1, player2, depth, alpha, beta)
#   else if next agent is MIN
#       return min-value(player1, player2, depth, alpha, beta)

# max-value:
#   v = -infinity
#   getSuccessorStates
#   for successor in successor states:
#       v = max(v, value(player1, player2, depth + 1, alpha, beta))
#       if v >= beta
#           return v
#       alpha = max(alpha, v)
#   return v

# min-value:
#   v = infinity
#   for successor in successor_states
#       v = min(v, value(player1, player2, depth + 1, alpha, beta))
#       if v <= alpha
#           return v
#       beta = min(beta, v)
#   return v


# Evaluation function
#   Terminal states
#   if player1 health == 0 and player2 health > 0
#       return -100
#   else if player2 health == 0 and player1 health > 0
#       return 100
# 
#   Non terminal states; check difference between health values; 