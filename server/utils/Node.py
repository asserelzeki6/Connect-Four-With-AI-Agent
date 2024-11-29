class Node:
    def __init__(self, board):
        self.board = board  # This should be the actual game board (a list or similar)
        self.children = []
        self.value = None
        self.move = None
        self.best_move = None

    def addChild(self, board, move):
        child = Node(board)  # Create a new node with a proper board
        child.move=move
        self.children.append(child)

    def set_value(self, value):
        self.value = value

    def set_best_move(self, best_move):
        self.best_move = best_move

    def get_board(self):
        return self.board

    def to_dict(self):
        return {
            'move': self.move,
            'best_move': self.best_move,
            'value': self.value,
            'children': [child.to_dict() for child in self.children]
        }
    def __str__(self):
        return f"Node(board={self.board})"

# board_data = [['', '', '', '', '', '', ''],
#               ['', '', '', '', '', '', ''],
#               ['', '', '', '', '', '', ''],
#               ['', '', '', '', '', '', ''],
#               ['', '', '', '', '', '', ''],
#               ['', '', '', '', '', '', '']]

# # Create a Node with the board data
# parent = Node(board_data)
# print("Parent board is: ", parent.board)  # This will now print the actual board
