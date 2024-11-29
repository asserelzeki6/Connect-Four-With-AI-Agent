// Node.js or TreeNode.js (frontend)

class Node {
    /**
     * @param {Object} param0
     * @param {any} param0.move
     * @param {any} param0.best_move
     * @param {any} param0.value
     * @param {Node[]} param0.children
     */
    constructor({ move = null, best_move = null, value = null, children = [] }) {
      this.move = move;              // Move that led to this node
      this.bestMove = best_move;     // Best move determined at this node
      this.value = value;            // Evaluation score
      this.children = children.map(child => new Node(child));  // Recursively create child nodes
    }
  
    // // Example method to find the best move in the tree
    // findBestMove() {
    //   if (!this.children.length) return this.move;  // Base case: return move if no children
    //   return this.children.reduce((best, child) =>
    //     child.value > (best?.value ?? -Infinity) ? child : best
    //   ).move;
    // }
  }
  
  export default Node;
  