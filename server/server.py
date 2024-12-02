# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from utils.minimax import minimax_without_pruning , minimax_with_pruning, expected_minimax
from utils.minimax import minimax_decision
from utils.expected import expected_decision
from utils.alphabeta import alphabeta_decision

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

    board = data['board']
    algorithm = data['algorithm']  # 'minimax', 'alphabeta', 'expected'
    maximumu_depth = data['maxDepth']
    aiPlayer = data['aiPlayer'] # 'r' or 'y'
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
        root=minimax_decision(board, aiPlayer, maximumu_depth)
    elif algorithm == 'alphaBeta':
        root=alphabeta_decision(board, aiPlayer, maximumu_depth)
    elif algorithm == 'expected':
        root=expected_decision(board, aiPlayer, maximumu_depth)
    else:
        print("unsupported algorithm")
        return
    

    print("best move is: ", root.best_move)
    Tree = root.to_dict()
    return jsonify(Tree)

if __name__ == '__main__':
    app.run(debug=True)
