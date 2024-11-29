<script>
    import { goto } from '$app/navigation';
    let playerChoice = 'r';  // Default player
    let algorithm = 'minimax';  // Default algorithm
    let rows = 6;
    let cols = 7;
    let showTree = false;
    let maxDepth = 4;

    function startGame() {
        const queryParams = new URLSearchParams({
            player: playerChoice,
            algorithm,
            rows: rows.toString(),
            cols: cols.toString(),
            maxDepth: maxDepth.toString(),
        });
        goto(`/connect-four?${queryParams.toString()}`);
    }
</script>

<svelte:head>
    <title>Connect Four</title>
</svelte:head>

<main>
    <h1>Welcome to Connect Four!</h1>
    <form on:submit|preventDefault={startGame} class="settings-form">
        <label>
            Choose Your Player:
            <select bind:value={playerChoice}>
                <option value="r">Player 1 (Red)</option>
                <option value="y">Player 2 (Yellow)</option>
            </select>
        </label>

        <label>
            AI Algorithm:
            <select bind:value={algorithm}>
                <option value="minimax">Minimax</option>
                <option value="alphaBeta">Minimax with Alpha-Beta Pruning</option>
                <option value="expected">Expected Minimax</option>
            </select>
        </label>

        <label>
            Board Rows: <input type="number" min="4" max="10" bind:value={rows} />
        </label>

        <label>
            Board Columns: <input type="number" min="4" max="10" bind:value={cols} />
        </label>

        <label>
            Max Tree Depth: <input type="number" min="1" max="10" bind:value={maxDepth} />
        </label>

        <button type="submit">Start Game</button>
    </form>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
    }
    h1 {
        margin-bottom: 1.5rem;
    }
    .settings-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        width: 300px;
    }
    label {
        display: flex;
        justify-content: space-between;
        font-size: 1.1rem;
    }
    input, select {
        padding: 0.5rem;
        font-size: 1rem;
    }
    button {
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.2rem;
    }
</style>
