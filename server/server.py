# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.minimax import minimax_without_pruning , minimax_with_pruning, expected_minimax
from utils.Node import Node

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/AI_move', methods=['get'])
def make_move():
    data = request.json
    # Extract necessary data (e.g., board state, player move)
    board = data['board']
    algorithm = data['algorithm']  # 'minimax', 'alphabeta', 'expected'
    maximumu_depth = data['maximum_depth']
    starting_player = data['starting_player']
    # Call your AI function here (placeholder response for now)
    best_move = None 
    Tree = None
    root = None
    best_value = None
    if algorithm == 'minimax':
        root, best_move, best_value=minimax_without_pruning(board, starting_player, maximumu_depth)
    elif algorithm == 'alphabeta':
        root, best_move, best_value=minimax_with_pruning(board, starting_player, maximumu_depth)
    elif algorithm == 'expected':
        root, best_move, best_value=expected_minimax(board, starting_player, maximumu_depth)
    else:
        print("unsupported algorithm")
        return
    
    print("best move is: ", best_move)
    print("best value is: ", best_value)
    Tree = root.to_dict

    return jsonify(Tree)

if __name__ == '__main__':
    app.run(debug=True)
