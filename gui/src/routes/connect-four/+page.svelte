
<script>
    import ConnectFour from '../../lib/components/ConnectFour.svelte';
    import { page } from '$app/stores';

    // Extract query parameters
    let params;
    $: {
        const { url } = $page;
        params = new URLSearchParams(url.search);
    }
    $: player = params.get('player') || 'Red';
    $: algorithm = params.get('algorithm') || 'Minimax';
    $: rows = parseInt(params.get('rows') || '6');
    $: cols = parseInt(params.get('cols') || 7);
    $: maxDepth = parseInt(params.get('maxDepth') || 4);
</script>

<main>
    <h1>Connect Four</h1>
    <div class="board">
      <ConnectFour {player} {algorithm} {rows} {cols} {maxDepth} />
    </div>
</main>

<style>
    .board {
        display: flex;
        justify-content: center;
        place-items: center;
        /* margin-top: 2rem; */
    }
</style>
