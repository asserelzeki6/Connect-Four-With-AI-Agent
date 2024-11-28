class Node:

    def __init__(self, board):
        self.board = board
        self.children = []
        self.value = None
        self.move = None
        self.best_move=None

    def addChild(self,board, move):
        child = Node(board)
        child.set_move(move)
        self.children.append(child)

    def set_value(self, value):
        self.value = value

    def set_best_move(self, best_move):
        self.best_move=best_move

    def to_dict(self):
        # Convert TreeNode to a dictionary for JSON serialization
        return {
            'move': self.move,
            'best_move' : self.best_move,
            'value': self.value,
            'children': [child.to_dict() for child in self.children]
        }