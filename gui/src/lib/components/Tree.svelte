<!-- TreeNode.svelte -->
<!-- <script>
    import Node from "$lib/Node";
    import TreeNode from "./TreeNode.svelte";
    export let node;  // Receive the current node as a prop

  </script>
   -->
  <!-- <div class="node">
    <p><strong>Move:</strong> {node.move} | <strong>Value:</strong> {node.value}</p>
  
    {#if node.children.length > 0}
      <ul>
        {#each node.children as child}
          <li><TreeNode node={child} /></li>   Recursively render children -->
        <!-- {/each}
      </ul>
    {/if}
  </div> --> 
  
  <!-- <style>
    .node { margin-left: 20px; }
    ul { list-style-type: none; padding-left: 0; }
  </style>
   -->

   <script>
    export let tree = null;  // This will be passed from the parent component
    /** @type {number | null} */
    export let bestMove = null; // Store the best move
    function renderTree(node) {
      return `
        <div style="margin-left: 20px;">
          <div>Move: ${node.move}</div>
          <div>Best Move: ${node.best_move}</div>
          <div>Value: ${node.value}</div>
          <div>
            ${node.children.map(renderTree).join('')}
          </div>
        </div>
      `;
    }
  </script>
  
  {#if tree}
    <div>
      <h3>Game Tree</h3>
      <div>
        <!-- Render the tree recursively -->
        {@html renderTree(tree)}
      </div>
      <h4>Best Move: {bestMove}</h4>
    </div>
  {:else}
    <p>No tree available</p>
  {/if}
  
  
  <style>
    div {
      margin-left: 20px;
      font-family: Arial, sans-serif;
    }
  
    h3, h4 {
      font-size: 18px;
    }
  
    div > div {
      margin-top: 10px;
    }
  </style>
  