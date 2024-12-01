import copy
from scoring import heuristic, print_board
from Nodev2 import Nodev2


def minimize(state, depth, max_depth):
    current_node = Nodev2(state, 'x', depth)
    best_child = None
    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'x')
        return current_node, None

    min_utility = float('inf')

    for child_board in get_children(state, 'x'):
        child_node, _ = maximize(child_board, depth + 1, max_depth)
        current_node.add_child(child_node)

        if child_node.utility < min_utility:
            min_utility = child_node.utility
            best_child = child_node

    current_node.utility = min_utility
    return current_node, best_child


def maximize(state, depth, max_depth):
    current_node = Nodev2(state, 'r', depth)
    best_child = None
    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'x')
        return current_node, None

    max_utility = float('-inf')

    for child_board in get_children(state, 'r'):
        child_node, _ = minimize(child_board, depth + 1, max_depth)
        current_node.add_child(child_node)

        if child_node.utility > max_utility:
            max_utility = child_node.utility
            best_child = child_node

    current_node.utility = max_utility
    return current_node, best_child


def decision(state):
    root_node, best_move = maximize(state, 0, 3)
    return root_node , best_move


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


if __name__ == "__main__":
    boardd = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'r', '.', '.'],
        ['.', '.', 'x', 'r', 'r', '.', '.'],
        ['.', '.', 'r', 'x', 'x', '.', '.'],
        ['x', 'r', 'r', 'r', 'x', 'x', 'x'],
        ['r', 'r', 'r', 'r', 'x', 'x', 'x']
    ]
    root, move = decision(boardd)
    print_board(move.board)
    print_tree(root)
