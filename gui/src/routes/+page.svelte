<script>
    import { gameSettings } from '../stores/gameSettings';
    import ConnectFour from '../lib/components/ConnectFour.svelte';

    let playerChoice = 'r';  // Default player
    let algorithm = 'minimax';  // Default algorithm
    let rows = 6;
    let cols = 7;
    let maxDepth = 2;

    let gameStarted = false;  // Flag to control the display of the game board

    // Update the store and start the game without navigation
    function startGame() {
        gameSettings.set({
            player: playerChoice,
            algorithm,
            rows,
            cols,
            maxDepth
        });

        gameStarted = true;  // Show the game once the settings are applied
    }

    // Go back to the main menu (reset the game state)
    function goBack() {
        gameStarted = false;  // Reset the game state to show the settings
        gameSettings.set({
            player: 'r',
            algorithm: 'minimax',
            rows: 6,
            cols: 7,
            maxDepth: 2
        });
    }
</script>

<svelte:head>
    <title>Connect Four</title>
</svelte:head>

<main>
    <h1>Welcome to Connect Four!</h1>

    {#if !gameStarted}
        <!-- Settings Section -->
        <div class="settings">
            <div class="player-selection">
                <button 
                    type="button" 
                    class="disc red" 
                    on:click={() => playerChoice = 'r'} 
                    class:selected={playerChoice === 'r'}>
                    <span>Red</span>
                </button>
                <button 
                    type="button" 
                    class="disc yellow" 
                    on:click={() => playerChoice = 'y'} 
                    class:selected={playerChoice === 'y'}>
                    <span>Yellow</span>
                </button>
            </div>

            <div class="setting-item">
                <label>AI Algorithm:</label>
                <select bind:value={algorithm}>
                    <option value="minimax">Minimax</option>
                    <option value="alphaBeta">Minimax with Alpha-Beta Pruning</option>
                    <option value="expected">Expected Minimax</option>
                </select>
            </div>

            <div class="setting-item">
                <label>Board Rows:</label>
                <input type="number" min="4" max="10" bind:value={rows} />
            </div>

            <div class="setting-item">
                <label>Board Columns:</label>
                <input type="number" min="4" max="10" bind:value={cols} />
            </div>

            <div class="setting-item">
                <label>Max Tree Depth:</label>
                <input type="number" min="1" max="10" bind:value={maxDepth} />
            </div>

            <button on:click={startGame}>Start Game</button>
        </div>
    {:else}
        <!-- Game Board -->
        <div class="board">
            <ConnectFour 
                player={$gameSettings.player} 
                algorithm={$gameSettings.algorithm} 
                rows={$gameSettings.rows} 
                cols={$gameSettings.cols} 
                maxDepth={$gameSettings.maxDepth} />
        </div>

        <!-- Go Back Button -->
        <button on:click={goBack}>Back to Settings</button>
    {/if}
</main>

<style>
    /* General Page Styling */
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        font-family: 'Arial', sans-serif;
        background-color: transparent;  /* Deep blue background for the page */
        color: white;
    }

    h1 {
        margin-bottom: 1.5rem;
        color: #ffcc00;  /* Yellow text for the header */
        font-size: 2.5rem;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
    }

    /* Settings Section Styling */
    .settings {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        width: 300px;
        padding: 1.5rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .setting-item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    label {
        font-size: 1.2rem;
        color: white;
    }

    .player-selection {
        display: flex;
        gap: 10px;
        justify-content: space-between;
    }

    .disc {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 1px solid #fff;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        color: white;
        font-size: 1rem;
        transition: transform 0.2s ease-in-out;
    }

    .red {
        background-color: #ff6347;  /* Red for Player 1 */
    }

    .yellow {
        background-color: #ffcc00;  /* Yellow for Player 2 */
        color: black;
    }

    .disc:hover {
        transform: scale(1.1);
        background-color: #1e3a5f;
    }

    .disc.selected {
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.6);
        transform: scale(1.3);
    }

    select, input {
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 5px;
        border: 2px solid #ffcc00;
        background-color: #1e3a5f;  /* Dark blue for inputs */
        color: white;
        transition: all 0.3s ease;
    }

    button {
        background-color: #ffcc00;  /* Yellow button */
        color: black;
        padding: 0.75rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.2rem;
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #ff6347;  /* Red on hover */
    }

    .board {
        display: flex;
        justify-content: center;
        place-items: center;
        margin-top: 2rem;
    }

    .board button {
        background-color: #ff6347;  /* Red board buttons */
        padding: 1rem;
        border-radius: 50%;
        margin: 5px;
    }
</style>
