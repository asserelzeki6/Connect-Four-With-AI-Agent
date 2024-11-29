<script>
    import { ENDPOINTS } from '../enpoints';
    import Node from '$lib/Node.js';  // Import the Node class
    import Tree from '$lib/components/Tree.svelte';  // Import the TreeDisplay component
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { on } from 'svelte/events';
    export let player;
    export let algorithm;
    export let rows;
    export let cols;
    export let maxDepth;
    export let tree = null;
    let player1_score = 0;
    let player2_score = 0;
    /** @type {number | null} */
    export let bestMove = null;
    let showTree = false;
    
    let board = Array.from({ length: rows }, () => Array(cols).fill('.'));
    const ROWS = 6;
    const COLS = 7;
    let currentPlayer = 'r';
    /** @type {string | null} */
    let winner = null;

    onMount(() => {
        if (player !== 'r') {
            AiMove(board, player, algorithm, maxDepth);
        }});
    
    async function AiMove(board, player, algorithm, maxDepth) {
        try {
            const payload = { 
                board, 
                starting_player : player, 
                algorithm, 
                maximum_depth : maxDepth 
            };
            const response = await fetch(ENDPOINTS.AIResponse, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const result = await response.json();
            console.log('Server response:', result);
            // tree = result.data;
            bestMove = result.best_move;
            tree = result;
            console.log('Best move:', bestMove);
            if (bestMove !== null) {
                dropDisc(bestMove);
            }
            /////////////////////////////
            // bestMove = result;
            //console.log('Best move:', bestMove);
            // if (bestMove !== null) {
            //     dropDisc(bestMove);
            // }
            //////////////////////////////////
            // Tree = new Node(result.data);
            // return Tree.move;
            // return result.data;
        } catch (error) {
            console.error('Error sending game data:', error);
        }
    }
    
    function toggleTree() {
        // //console.log('Show tree');
        showTree = !showTree;
    }

    function dropDisc(col=0) {
        if (winner) return;
        //console.log(board);
        //console.log('Dropping disc in column:', col);
        check_endgame();
        for (let row = ROWS - 1; row >= 0; row--) {
            if (board[row][col]==='.') {
                board[row][col] = currentPlayer;
                // if (checkWinner()) {
                //     winner = currentPlayer;
                // } else {
                //console.log('Current player:', currentPlayer);
                calculateScore(currentPlayer, row, col);
                currentPlayer = currentPlayer === 'r' ? 'y' : 'r';
                if (check_endgame())
                    return;
                if (currentPlayer !== player) {
                    AiMove(board, player, algorithm, maxDepth);
                }
                break;
            }
        }
    }

    function check_endgame() {
        let row = board.length;
        let col = board[0].length;
        console.log(board);
        for(let i = 0; i < col; i++) {
            if (board[0][i] === '.') {
                console.log('not full as', board[0][i]);
                return false;
            }
        }
        if (player1_score > player2_score) {
            winner = 'player1'
        } else if (player1_score < player2_score) {
            winner = 'player2'
        } else {
            winner = 'tie'
        }
        console.log('endgame');
        return true;
    }


    function calculateScore(currentPlayer, i, j) {
        let row = board.length;
        let col = board[0].length;
        // if (winner === 'r') {
        //     player1_score++;
        // } else if (winner === 'y') {
        //     player2_score++;
        // }
        let hr=1
        let hl=1
        let vu=1
        let vd=1
        let dlu=1
        let dru=1
        let dld=1
        let drd=1
        let moves = [1,2,3]
        let added_score = 0
        for (let k in moves) {
            if (j+k<col){ // horizontal right
                if (board[i][j+k]===currentPlayer)
                    hr+=1
                else
                    hr=0
                if (i-k>=0){ // diagonal right up
                    if (board[i-k][j+k]==currentPlayer)
                        dru+=1
                    else
                        dru=0
                }
            }
            if (i - k >= 0) { // vertical up
                if (board[i - k][j] === currentPlayer) {
                    vu++;
                } else {
                    vu = 0;
                }
                if (j - k >= 0) { // diagonal left up
                    if (board[i - k][j - k] === currentPlayer) {
                        dlu++;
                    } else {
                        dlu = 0;
                    }
                }
            }

            if (j - k >= 0) { // horizontal left
                if (board[i][j - k] === currentPlayer) {
                    hl++;
                } else {
                    hl = 0;
                }
                if (i - k >= 0) { // diagonal right down
                    if (board[i - k][j - k] === currentPlayer) {
                        drd++;
                    } else {
                        drd = 0;
                    }
                }
            }

            if (i + k < row) { // vertical down
                if (board[i + k][j] === currentPlayer) {
                    vd++;
                } else {
                    vd = 0;
                }
                if (j - k >= 0) { // diagonal left down
                    if (board[i + k][j - k] === currentPlayer) {
                        dld++;
                    } else {
                        dld = 0;
                    }
                }
            }
        }

        if (hr === 4) added_score += 1;
        if (vu === 4) added_score += 1;
        if (dru === 4) added_score += 1;
        if (dlu === 4) added_score += 1;
        if (hl === 4) added_score += 1;
        if (vd === 4) added_score += 1;
        if (drd === 4) added_score += 1;
        if (dld === 4) added_score += 1;
        if (added_score > 0) {
            if (currentPlayer === 'r') {
                player1_score += added_score;
            } else {
                player2_score += added_score;
            }
        }
    }
    function resetGame() {
        board = Array.from({ length: ROWS }, () => Array(COLS).fill(null));
        currentPlayer = 'r';
        winner = null;
        if (player !== 'r') {
            AiMove(board, player, algorithm, maxDepth);
        }
    }
    export function goBack() {
        resetGame();
        // redirect(302,'/');
        goto('/');
    }
</script>

<style>
    .board {
        display: grid;
        grid-template-columns: repeat(7, 50px);
        gap: 5px;
    }
    .cell {
        width: 50px;
        height: 50px;
        background-color: #4a0ce6;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .disc {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    .r {
        background-color: red;
    }
    .y {
        background-color: yellow;
    }
</style>

<div>
    <div class="board">
        {#each board as row, rowIndex}
            {#each row as cell, colIndex}
                <div class="cell" role="button" tabindex="0" on:click={() => dropDisc(colIndex)} on:keydown={(e) => e.key === 'Enter' && dropDisc(colIndex)}>
                    {#if cell !== '.'}
                        <div class="disc {cell}"></div>
                    {/if}
                </div>
            {/each}
        {/each}
    </div>
    <button on:click={resetGame}>Reset Game</button>
    <button on:click={toggleTree}>Show Tree</button>
    <button on:click={goBack}>Go back to main menu</button>
    <div>
        <p>Player 1 (Red) Score: {player1_score}</p>
        <p>Player 2 (Yellow) Score: {player2_score}</p>
    </div>
    {#if winner}
        {#if winner === 'tie'}
            <h2>It's a tie!</h2>
        {:else}
            <h2>{winner} wins!</h2>
        {/if}
    {/if}
    {#if showTree}
        <Tree {tree} /> 
    {/if}

</div>