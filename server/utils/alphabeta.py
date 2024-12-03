import sys
import os
from graphviz import Digraph

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.utils.scoring import heuristic, print_board
from server.utils.Node import Node
from server.utils.tree import get_children, print_tree, generate_children

def minimize(current_node, depth, max_depth, alpha, beta):
    state = current_node.board
    best_child = None
    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    min_utility = float('inf')

    for child in generate_children(state, 'y', depth+1):
        _, _ = maximize(child, depth + 1, max_depth, alpha, beta)
        current_node.add_child(child)

        if child.utility < min_utility:
            min_utility = child.utility
            best_child = child

        if min_utility <= alpha:
            break

        if min_utility < beta:
            beta = min_utility

    if best_child is None:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    current_node.best_move = best_child.move
    current_node.utility = min_utility
    return current_node, best_child

def maximize(current_node, depth, max_depth, alpha, beta):
    state = current_node.board
    
    best_child = None

    if depth == max_depth:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None

    max_utility = float('-inf')

    for child in generate_children(state, 'r', depth+1):
        _, _ = minimize(child, depth + 1, max_depth, alpha, beta)
        current_node.add_child(child)

        if child.utility > max_utility:
            max_utility = child.utility
            best_child = child

        if max_utility >= beta:
            break

        if max_utility > alpha:
            alpha = max_utility

    if best_child is None:
        current_node.utility = heuristic(state, 'r', 'y')
        return current_node, None
    
    current_node.best_move = best_child.move
    current_node.utility = max_utility
    return current_node, best_child

def alphabeta_decision(state, aiPlayer,max_depth):
    root_node = Node(state, aiPlayer, 0)
    if aiPlayer == 'r':
        root_node, best_child = maximize(root_node, 0, max_depth, float('-inf'), float('inf'))
    else:
        root_node, best_child = minimize(root_node, 0, max_depth, float('-inf'), float('inf'))
    root_node.isRoot = True
    return root_node, best_child

def visualize_tree(node, filename="tree_visualization"):
    graph = Digraph(format="png", graph_attr={"rankdir": "TB"})  # Top-to-Bottom layout

    def add_nodes_edges(graph, node):

        node_id = id(node)  # Unique ID based on the node's memory address
        graph.node(
            str(node_id),
            f"Depth: {node.depth}\nPlayer: {node.player}\nUtility: {node.utility}",
            shape="box",
        )
        for child in node.children:
            child_id = id(child)
            graph.edge(str(node_id), str(child_id))
            add_nodes_edges(graph, child)

    add_nodes_edges(graph, node)
    graph.render(filename, cleanup=True)
    print(f"Tree visualized and saved as {filename}.png")

if __name__ == "__main__":
    boardd = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
    ]
    root, move = alphabeta_decision(boardd,'r',8)
    print_board(move.board)
    print_tree(root)
    visualize_tree(root)
