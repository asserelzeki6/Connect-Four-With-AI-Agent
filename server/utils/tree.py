import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Node import Node 
from utils.scoring import *
import copy

empty = '.'

def generate_tree(root:Node, starting_player, player1, player2, max_height):
    # root = Node(board)
    recursive_generation_tree(root, starting_player, max_height,player1, player2)
    return root


def recursive_generation_tree(root:Node, player, max_height,player1,player2):
    if max_height==0 : 
        root.set_value(board_score(root.board,player1,player2)) #### CHANGE HERE THE HEURISTIC 
        return
    generate_children(root,player)
    if player == player1:
        player=player2
    else:
        player=player1
    for child in root.children:
        recursive_generation_tree(child,player,max_height-1,player1,player2)
    if len(root.children) == 0:
        root.set_value(board_score(root.board,player1,player2))

def generate_children(parent:Node, player):
    # print("Parent board type is: ", type(parent.board))
    # print("Parent board is: ", parent.board)
    # print("Parent board row is: ", len(parent.board))
    # print("Parent board col is: ", len(parent.board[0]))
    board=parent.board
    col=len(board[0])
    for j in range(col):
        r = playable_row(board, j)
        if r != -1:
            new_board = copy.deepcopy(board)
            new_board[r][j]=player
            move = j
            # print(f"Adding child for player {player} at row {r}, column {j}")
            parent.addChild(new_board, move)
        # else:
            # print(f"Column {j} is full, skipping this move.")

def playable_row(board, j):
    row = len(board)
    for i in range(row-1,-1,-1):
        if board[i][j] == empty:
            return i
    return -1

def make_tree_printable(root:Node):
    pass