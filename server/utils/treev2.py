import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Chance import Chance
from utils.Nodev2 import Nodev2
import copy

def get_children(board, player):
    col = len(board[0])
    children = []
    for j in range(col):
        r = playable_row(board, j)
        if r != -1:
            new_board = copy.deepcopy(board)
            new_board[r][j] = player
            children.append(new_board)
    return children

def get_expected_children(board, player, children, depth):
    col = len(board[0])
    expected_children = []
    for j in range(col):
        child = None
        prev_child = None
        next_child = None
        for c in children:
            if c.move == j:
                child = c
            if c.move == j-1:
                prev_child = c
            if c.move == j+1:
                next_child = c
        if child is not None:
            chance = Chance(j,player,depth)
            chance.add_children(child,prev_child,next_child)
            chance.calculate_utility()
            expected_children.append(chance)
    return expected_children

def generate_children(board, player, depth):
    col=len(board[0])
    children = []
    for j in range(col):
        r = playable_row(board, j)
        if r != -1:
            new_board = copy.deepcopy(board)
            new_board[r][j]=player
            move = j
            current_node = Nodev2(new_board, player, depth)
            current_node.move = move
            children.append(current_node)
    return children

def playable_row(board, j):
    row = len(board)
    for i in range(row - 1, -1, -1):
        if board[i][j] == '.':
            return i
    return -1


def print_tree(node, depth=0):
    prefix = "    " * depth
    print(f"{prefix}Depth: {node.depth}, Player: {node.player}, Utility: {node.utility}")
    for child in node.children:
        print_tree(child, depth + 1)
