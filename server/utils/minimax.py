import sys
import os

# Add the project's root directory to the Python path

import copy
from server.utils.scoring import heuristic, print_board
from server.utils.Node import Node
from server.utils.tree import get_children, print_tree, generate_children
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def minimize(current_node, depth, max_depth):
    state = current_node.board
    best_child = None
    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    min_utility = float('inf')

    for child in generate_children(state, 'y', depth+1):
        _, _ = maximize(child, depth + 1, max_depth)
        current_node.add_child(child)

        if child.utility < min_utility:
            min_utility = child.utility
            best_child = child

    if best_child is None:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None
    
    current_node.best_move = best_child.move
    current_node.utility = min_utility
    return current_node, best_child


def maximize(current_node, depth, max_depth):
    state = current_node.board
    best_child = None
    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    max_utility = float('-inf')

    for child in generate_children(state, 'r', depth+1):
        _, _ = minimize(child, depth + 1, max_depth)
        current_node.add_child(child)

        if child.utility > max_utility:
            max_utility = child.utility
            best_child = child

    if best_child is None:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    current_node.best_move = best_child.move
    current_node.utility = max_utility
    return current_node, best_child


def minimax_decision(state, aiPlayer,max_depth):
    root_node = Node(state, aiPlayer, 0)
    if aiPlayer == 'r':
        root_node, best_child = maximize(root_node, 0, max_depth)
    else:
        root_node, best_child = minimize(root_node, 0, max_depth)
    root_node.isRoot = True
    return root_node, best_child



if __name__ == "__main__":
    boardd = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
    ]
    root, move = minimax_decision(boardd,'r',4)
    print_board(move.board)
    print_tree(root)

