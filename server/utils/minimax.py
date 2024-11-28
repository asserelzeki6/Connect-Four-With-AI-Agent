import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Node import Node
from utils.tree import generate_tree

player1='r'
player2='y'

##########################MINIMAX WITHOUT PRUNING#############################
def minimax_without_pruning(board, starting_player, max_height):
    root = Node(board)
    generate_tree(root, starting_player, player1, player2, max_height)

    best_state:Node = None
    best_value = 0

    if starting_player == player1:
        best_state, best_value = max_without_pruning(root)
    else:
        best_state, best_value = min_without_pruning(root)

    return root, best_state.move, best_value

def max_without_pruning(state:Node):
    if state.value != None:
        return state, state.value
    
    max_child = None
    max_value = float('-inf')
    best_move = None

    for child in state.children:
        _, value = min_without_pruning(child)
        if value > max_value:
            best_move, max_child, max_value = child.move , child, value
    
    state.set_best_move(best_move)
    state.set_value(max_value)
    return max_child, max_value

def min_without_pruning(state:Node):
    if state.value != None:
        return state, state.value
    
    min_child = None
    min_value = float('inf')
    best_move = None

    for child in state.children:
        value = max_without_pruning(child)
        if value < min_value:
            best_move, min_child, min_value = child.move, child, value

    state.set_best_move(best_move)
    state.set_value(min_value)
    return min_child, min_value
    
#########################MINIMAX WITH PRUNING#################################
def minimax_with_pruning(board, starting_player, max_height):
    root = Node(board)
    generate_tree(root, starting_player, player1, player2, max_height)

    best_state:Node = None
    best_value = 0

    if starting_player == player1:
        best_state, best_value = max_with_pruning(root, float('-inf'), float('inf'))
    else:
        best_state, best_value = min_with_pruning(root, float('-inf'), float('inf'))

    return root, best_state.move, best_value

def max_with_pruning(state:Node, alpha, beta):
    if state.value != None:
        return state,state.value
    
    max_child = None
    max_value = float('-inf')
    best_move = None

    for child in state.children:
        _, value = min_with_pruning(child, alpha, beta) 
        if value > max_value:
            best_move, max_child, max_value = child.move, child, value
        if max_value >= beta:
            break
        if max_value > alpha:
            alpha = max_value

    state.set_best_move(best_move)
    state.set_value(max_value)
    return max_child, max_value

def min_with_pruning(state:Node, alpha, beta):
    if state.value != None:
        return state, state.value
    
    min_child=None
    min_value=float('inf')    
    best_move = None

    for child in state.children:
        _, value = max_with_pruning(child, alpha, beta)
        if value < min_value:
            best_move, min_child, min_value = child.move, child, value
        if min_value <= alpha:
            break
        if min_value < beta:
            beta = min_value

    state.set_best_move(best_move)
    state.set_value(min_value)
    return min_child, min_value
    
###########################EXPECTED MINIMAX####################################
def expected_minimax(board, starting_player, max_height):
    root = Node(board)
    generate_tree(root, starting_player, player1, player2, max_height)

    best_state:Node = None
    best_value = 0

    if starting_player == player1:
        best_state, best_value = expected_max(root)
    else:
        best_state, best_value = expected_min(root)

    return root, best_state.move, best_value

def expected_max(state:Node):
    if state.value != None:
        return state, state.value
    
    n = len(state.children)
    max_child_index=0
    values=[]
    max_child = None
    max_value = float('-inf')
    best_move = None

    for i in range(n):
        _, value = expected_min(state.children[i])
        values.append(value)
        if value > max_value:
            best_move, max_child_index, max_child, max_value = state.children[i].move, i, state.children[i], value

    expected_value = 0.6*max_value
    if max_child_index-1 >= 0:
        expected_value+=0.2*values[max_child_index-1]
    else:
        expected_value+=0.2*max_value
    if max_child_index+1 < n:
         expected_value+=0.2*values[max_child_index+1]
    else:
        expected_value+=0.2*max_value

    state.set_best_move(best_move)
    state.set_value(expected_value)
    return max_child, expected_value

def expected_min(state:Node):
    if state.value != None:
        return state, state.value
    
    n = len(state.children)
    min_child_index=0
    values=[]
    min_child = None
    min_value = float('inf')
    best_move = None

    for i in range(n):
        _, value = expected_max(state.children[i])
        values.append(value)
        if value < min_value:
            best_move, min_child_index, min_child, min_value = state.children[i].move, i, state.children[i], value

    expected_value = 0.6*min_value
    if min_child_index-1 >= 0:
        expected_value+=0.2*values[min_child_index-1]
    else:
        expected_value+=0.2*min_value
    if min_child_index+1 < n:
         expected_value+=0.2*values[min_child_index+1]
    else:
        expected_value+=0.2*min_value

    state.set_best_move(best_move)
    state.set_value(expected_value)
    return min_child, expected_value