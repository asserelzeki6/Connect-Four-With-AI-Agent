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
        self.move = None
        self.utility = None
        self.best_move = None
        self.isRoot = False

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        if self.isRoot:
            return {
                'type': 'Root',
                'player': self.player,
                'depth': self.depth,
                'children': [child.to_dict() for child in self.children],
                'move': self.move,
                'best_move': self.best_move, 
                'utility': self.utility
            }
        return {
            'type': 'Node',
            'player': self.player,
            'depth': self.depth,
            'children': [child.to_dict() for child in self.children],
            'move': self.move,
            'best_move': self.best_move, 
            'utility': self.utility
        }