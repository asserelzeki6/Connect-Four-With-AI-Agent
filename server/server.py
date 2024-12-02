# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from utils.minimax import minimax_without_pruning , minimax_with_pruning, expected_minimax
from utils.minimaxv2 import minimax_decision
from utils.expectedv2 import expected_decision
from utils.alphabetav2 import alphabeta_decision

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/game/ai-response', methods=['post'])
def make_move():
    print("request is: ", request)
    if not request.json:
        print("request is not json")
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    # print("data is: ", data)
    # Extract necessary data (e.g., board state, player move)
    board = data['board']
    algorithm = data['algorithm']  # 'minimax', 'alphabeta', 'expected'
    maximumu_depth = data['maxDepth']
    aiPlayer = data['aiPlayer']
    # Call your AI function here (placeholder response for now)
    print("board is: ")
    for i in board:
        print(i)
    print("algorithm is: ", algorithm)
    print("maximumu depth is: ", maximumu_depth)
    print("ai Player is: ", aiPlayer)
    best_move = None 
    Tree = None
    root = None
    best_value = None
    if algorithm == 'minimax':
        # root, best_move, best_value=minimax_without_pruning(board, starting_player, maximumu_depth)
        root=minimax_decision(board, aiPlayer, maximumu_depth)
    elif algorithm == 'alphaBeta':
        # root, best_move, best_value=minimax_with_pruning(board, starting_player, maximumu_depth)
        root=alphabeta_decision(board, aiPlayer, maximumu_depth)
    elif algorithm == 'expected':
        # root, best_move, best_value=expected_minimax(board, starting_player, maximumu_depth)
        root=expected_decision(board, aiPlayer, maximumu_depth)
    else:
        print("unsupported algorithm")
        return
    
    # root = Node(board)
    # print("root is: ", root)
    # print(root.board)
    # print("row",len(root.board))
    # print("col",len(root.board[0]))

    print("best move is: ", root.best_move)
    Tree = root.to_dict()
    # print("Tree is: ", Tree)
    return jsonify(Tree)

    # best_move = 0
    # print("best move is: ", best_move)
    # return jsonify(best_move)

if __name__ == '__main__':
    app.run(debug=True)
