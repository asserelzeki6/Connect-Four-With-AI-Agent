<script>
    import { ENDPOINTS } from '../enpoints';
    import Tree from '$lib/components/Tree.svelte';  // Import the TreeDisplay component
    import { onMount } from 'svelte';
    
    export let player;
    export let algorithm;
    export let rows;
    export let cols;
    export let maxDepth;
    export let tree = null;
    /** @type {number | null} */
    export let bestMove = null;
    let showTree = false;
    
    let board = Array.from({ length: rows }, () => Array(cols).fill('.'));
    let currentPlayer = 'r';  // Default: red (human)
    /** @type {string | null} */
    let winner = null;
    let player1_connectedFours = 0;  // Track connected fours for player 1
    let player2_connectedFours = 0;  // Track connected fours for player 2
    let aiPlayer = 'y';  // Default: yellow (AI)
  
// Initialization based on player's choice
onMount(() => {
    console.log('Game started with:', { player, algorithm, rows, cols, maxDepth });
    
    // If player chooses red ('r'), they start, AI is yellow ('y')
    if (player === 'r') {
        currentPlayer = 'r'; // Player starts with red
        aiPlayer = 'y'; // AI is yellow
    } 
    // If player chooses yellow ('y'), AI starts with red
    else if (player === 'y') {
        currentPlayer = 'r'; // Player starts with yellow
        aiPlayer = 'r'; // AI is red
        AiMove(board, aiPlayer, algorithm, maxDepth);  // AI starts first
    }
});

// AI move function based on assigned role (red or yellow)
async function AiMove(board, aiPlayer, algorithm, maxDepth) {
    try {
        const payload = { 
            board, 
            starting_player: aiPlayer, 
            algorithm, 
            maximum_depth: maxDepth 
        };
        const response = await fetch(ENDPOINTS.AIResponse, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        bestMove = result.best_move;
        tree = result;
        if (bestMove !== null) dropDiscAI(bestMove);  // Make AI move
    } catch (error) {
        console.error('Error sending game data:', error);
        setTimeout(() => {}, 500);
        if (currentPlayer !== player) AiMove(board, player, algorithm, maxDepth);
    }
}

// AI makes a move based on its assigned color
function dropDiscAI(col=0) {
    if (currentPlayer === aiPlayer && winner === null) {
        for (let row = rows - 1; row >= 0; row--) {
            if (board[row][col] === '.') {
                board[row][col] = aiPlayer;  // AI drops the correct colored disc
                calculateScore(aiPlayer, row, col);
                if (check_endgame()) return;
                currentPlayer = (aiPlayer === 'r') ? 'y' : 'r';  // Switch to player
                break;
            }
        }
    }
}

// Handle the human player's move
function dropDiscHuman(col=0) {
    if(showTree)
        toggleTree();
    if (currentPlayer === player && winner === null) {
        for (let row = rows - 1; row >= 0; row--) {
            if (board[row][col] === '.') {
                board[row][col] = player;  // Player drops their colored disc
                calculateScore(player, row, col);
                if (check_endgame()) return;
                currentPlayer = aiPlayer;  // Switch to AI
                if (currentPlayer === aiPlayer) {
                    setTimeout(() => { 
                        AiMove(board, aiPlayer, algorithm, maxDepth); 
                    }, 500);  // Delay AI move for smoother gameplay
                }
                break;
            }
        }
    }
}


    function check_endgame() {
        if (board.every(row => row.every(cell => cell !== '.'))) {
            winner = player1_connectedFours > player2_connectedFours ? 'player1' :
                     player1_connectedFours < player2_connectedFours ? 'player2' : 'tie';
            return true;
        }
        return false;
    }
  
    function calculateScore(currentPlayer, i, j) {
        const directions = [
            { dx: 1, dy: 0 },  // Horizontal
            { dx: 0, dy: 1 },  // Vertical
            { dx: 1, dy: 1 },  // Diagonal down-right
            { dx: 1, dy: -1 }, // Diagonal up-right
        ];
  
        let added_score = 0;
        directions.forEach(({ dx, dy }) => {
            let count = 1;
            for (let k = 1; k < 4; k++) {
                const x = i + dx * k;
                const y = j + dy * k;
                if (x >= 0 && x < rows && y >= 0 && y < cols && board[x][y] === currentPlayer) {
                    count++;
                } else break;
            }
            for (let k = 1; k < 4; k++) {
                const x = i - dx * k;
                const y = j - dy * k;
                if (x >= 0 && x < rows && y >= 0 && y < cols && board[x][y] === currentPlayer) {
                    count++;
                } else break;
            }
            if (count >= 4) added_score++;
        });
  
        if (added_score > 0) {
            if (currentPlayer === 'r') player1_connectedFours += added_score;
            else player2_connectedFours += added_score;
        }
    }
  
    function resetGame() {
        board = Array.from({ length: rows }, () => Array(cols).fill('.'));
        currentPlayer = player === 'r' ? 'r' : 'y';  // Player starts based on selection
        winner = null;
        player1_connectedFours = 0;
        player2_connectedFours = 0;
        if (player === 'y') AiMove(board, 'r', algorithm, maxDepth);  // AI starts if player is yellow
    }
  
    function toggleTree() {
        showTree = !showTree;
    }
</script>

<div class="container">
    <div class="board-wrapper">
        <div class="board" style="grid-template-columns: repeat({board[0].length}, 70px);">
            {#each board as row, rowIndex}
                {#each row as cell, colIndex}
                    <div class="cell" role="button" tabindex="0" 
                        on:click={() => dropDiscHuman(colIndex)} 
                        on:keydown={(e) => e.key === 'Enter' && dropDiscHuman(colIndex)}>
                        {#if cell !== '.'}
                            <div class="disc {cell}"></div>
                        {/if}
                    </div>
                {/each}
            {/each}
        </div>
        <div class="board-stand"></div>  <!-- Stand beneath the board -->
    </div>

    <div class="scoreboard">
        <p class="player1">Player 1 (Red) Connected Fours: {player1_connectedFours}</p>
        <p class="player2">Player 2 (Yellow) Connected Fours: {player2_connectedFours}</p>
    </div>
    

    {#if winner}
        <h2>{#if winner === 'tie'}It's a tie!{:else}{winner} wins!{/if}</h2>
    {/if}

    <div class="buttons">
        <button on:click={resetGame}>Reset Game</button>
        <button on:click={toggleTree}>
            {showTree ? 'Hide Tree' : 'Show Tree'}
        </button>
    </div>
    
    <div>
        {#if showTree}
            <Tree {tree} />
        {/if}
    </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    margin-top: 20px;
}

.board-wrapper {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    position: relative;
}

.board {
    display: grid;
    /* grid-template-columns: repeat(cols, 70px); */
    gap: 10px;
    background-color: #0044cc;  /* Blue board background */
    padding: 10px;
    border-radius: 10px;
    width: max-content; /* Ensures width adjusts based on grid size */
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);  /* Add shadow to create a 3D effect */
    z-index: 1;
}

.board-stand {
    width: 100%;
    height: 50px;
    background-color: #333;  /* Dark brown or black color for the stand */
    position: absolute;
    bottom: -50px;
    left: 0;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);  /* Stand shadow for 3D look */
}

.cell {
    width: 70px;
    height: 70px;
    background-color: #acd3d8;  /* Dark blue cells for contrast */
    border-radius: 50%;
    position: relative;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cell:focus {
    outline: none;
}

.disc {
    width: 60px;
    height: 60px;
    background-color: transparent;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.disc.r {
    background-color: red;
}

.disc.y {
    background-color: yellow;
}

/* Update scoreboard styles */
.scoreboard {
    font-size: 1.5em;  /* Increase font size */
    font-weight: bold;
    font-family: 'Arial', sans-serif;  /* Change font to a clean, modern style */
    margin-top: 20px;  /* Move text down */
}

.scoreboard p {
    margin: 5px 0;
}

/* Player 1 (Red) score */
.scoreboard .player1 {
    color: red;  /* Set color to red for Player 1 */
}

/* Player 2 (Yellow) score */
.scoreboard .player2 {
    color: yellow;  /* Set color to yellow for Player 2 */
}


/* Update the buttons */
.buttons button {
    padding: 10px 15px;
    margin: 5px;
    font-size: 1.2em;  /* Increase font size */
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-family: 'Arial', sans-serif;  /* Clean font for buttons */
}

.buttons button:hover {
    background-color: #005a8b;
}

.buttons button:focus {
    outline: none;
}

/* Header text for the winner announcement */
h2 {
    font-size: 2em;  /* Larger font size for winner text */
    color: #f39c12;  /* Gold color for winner announcement */
    font-family: 'Arial', sans-serif;
    margin-top: 20px;  /* Add space above the text */
    text-align: center;
}

</style>
