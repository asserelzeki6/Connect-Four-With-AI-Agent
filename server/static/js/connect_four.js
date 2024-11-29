const rows = 6;
const cols = 7;
let board = Array.from({ length: rows }, () => Array(cols).fill('.'));
let currentPlayer = 'R';

// Initialize game board UI
function renderBoard() {
  const gameBoard = document.getElementById("game-board");
  gameBoard.innerHTML = "";
  board.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      const cellElement = document.createElement("div");
      cellElement.className = `cell ${cell}`;
      cellElement.onclick = () => makeMove(colIndex);
      gameBoard.appendChild(cellElement);
    });
  });
}

// Handle player move
async function makeMove(col) {
  for (let row = rows - 1; row >= 0; row--) {
    if (board[row][col] === '.') {
      board[row][col] = currentPlayer;
      currentPlayer = currentPlayer === 'R' ? 'Y' : 'R';
      renderBoard();

      // Fetch AI move from backend
      const response = await fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board })
      });
      const data = await response.json();
      board[data.row][data.column] = 'Y';
      renderBoard();
      break;
    }
  }
}

renderBoard();  // Initial render
