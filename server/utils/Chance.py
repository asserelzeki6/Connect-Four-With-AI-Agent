class Chance:
    def __init__(self, move, player, depth):

        # print_board(board)
        # print()
        self.player = player
        self.depth = depth
        self.move = move
        self.child = None
        self.prevChild = None
        self.nextChild = None
        self.utility = None
        self.children = []
        
    def add_children(self, child, prevChild=None, afterChild=None):
        self.child=child
        self.prevChild=prevChild
        self.nextChild=afterChild
        self.children.append(child)
        if prevChild is not None:
            self.children.append(prevChild)
        if afterChild is not None:
            self.children.append(afterChild)

    def calculate_utility(self):
        self.utility = self.child.utility * 0.6
        if self.prevChild is not None:
            self.utility += self.prevChild.utility * 0.2
        else:
            self.utility += self.child.utility * 0.2
        if self.nextChild is not None:
            self.utility += self.nextChild.utility * 0.2
        else:
            self.utility += self.child.utility * 0.2
        return round(self.utility,2)
    
    def to_dict(self):
        # Convert TreeNode to a dictionary for JSON serialization
        return {
            'type': 'Chance',
            'move': self.move,
            'utility': self.utility,
            'best_move': None,
            'children': [child.to_dict() for child in self.children]
        }

