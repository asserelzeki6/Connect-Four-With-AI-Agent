import { writable } from 'svelte/store';

export const gameSettings = writable({
    player: 'r',       // Default: Player 1 (Red)
    algorithm: 'minimax',
    rows: 6,
    cols: 7,
    maxDepth: 2
});
