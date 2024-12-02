import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from  utils.scoring import heuristic, print_board
from  utils.Node import Node
from  utils.tree import generate_children, print_tree, get_expected_children

def minimize(current_node, depth, max_depth):
    if depth >= max_depth:
        current_node.utility = heuristic(current_node.board, 'r', 'y')
        return current_node, None

    best_expected_child = None
    children = []
    for child in generate_children(current_node.board, 'y', depth+2):
        _, _ = minimize(child, depth + 2, max_depth)
        children.append(child)

    if len(children) == 0:
        current_node.utility = heuristic(current_node.board, 'r', 'y')
        return current_node, None
    
    best_expected_child, min_utility = minExpectedUtility(current_node, depth+1, 'y', children)
    current_node.best_move = best_expected_child.move
    current_node.utility = round(min_utility, 2)

    return best_expected_child, min_utility


def maximize(current_node, depth, max_depth):
    if depth >= max_depth:
        current_node.utility = heuristic(current_node.board, 'r', 'y')
        return current_node, None

    best_expected_child = None
    children = []
    for child in generate_children(current_node.board, 'r', depth+2):
        _, _ = minimize(child, depth + 2, max_depth)
        children.append(child)

    if len(children) == 0:
        current_node.utility = heuristic(current_node.board, 'r', 'y')
        return current_node, None
    
    best_expected_child, max_utility = maxExpectedUtility(current_node, depth+1, 'r', children)
    current_node.best_move = best_expected_child.move
    current_node.utility = round(max_utility,2)

    return best_expected_child, max_utility

def maxExpectedUtility(state, depth, player, children):
    best_expected_child = None
    maximum_expected_utility = float("-inf")
    for child in get_expected_children(state.board, player, children, depth):
        if child.utility > maximum_expected_utility:
            maximum_expected_utility = child.utility
            best_expected_child = child
        state.children.append(child)
    
    return best_expected_child, maximum_expected_utility


def minExpectedUtility(state, depth, player, children):
    best_expected_child = None
    minimum_expected_utility = float("inf")
    for child in get_expected_children(state.board, player, children, depth):
        if child.utility < minimum_expected_utility:
            minimum_expected_utility = child.utility
            best_expected_child = child
        state.children.append(child)

    return best_expected_child, minimum_expected_utility


def expected_decision(state, aiPlayer,max_depth):
    root_node = Node(state, aiPlayer, 0)
    if aiPlayer == 'r':
        _, _ = maximize(root_node, 0, max_depth)
    else:
        _, _ = minimize(root_node, 0, max_depth)
    root_node.isRoot = True
    return root_node 

# if __name__ == "__main__":
#     boardd = [
#         ['.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', 'r', '.', '.'],
#         ['.', '.', 'y', 'r', 'r', '.', '.'],
#         ['.', '.', 'r', 'y', 'y', '.', '.'],
#         ['y', 'r', 'r', 'r', 'y', 'y', 'y'],
#         ['r', 'r', 'r', 'r', 'y', 'y', 'y']
#     ]
#     root, move = decision(boardd, 'r','y', 3)
#     print_board(root.board)
#     print_tree(root)