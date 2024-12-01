import copy

class Nodev2:
    def __init__(self, board, player, depth):
        # Store the board state for this node

        self.board = copy.deepcopy(board)  # Ensure the board is not shared among nodes
        # print_board(board)
        # print()
        self.player = player
        self.depth = depth
        self.children = []
        self.utility = None

    def add_child(self, child):
        self.children.append(child)

