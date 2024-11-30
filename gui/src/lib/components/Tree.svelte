<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let tree = null;  // Passed from the parent

  let svgContainer;

  onMount(() => {
    if (tree) {
      drawTree(tree);
    }
  });

  function drawTree(data) {
    d3.select(svgContainer).selectAll("*").remove();  // Clear previous content

    const width = 1500;  // Increased width for better spacing
    const height = 800;  // Increased height for better spacing

    const svg = d3.select(svgContainer)
                  .attr("width", width)
                  .attr("height", height)
                  .append("g")
                  .attr("transform", "translate(50,50)");  // Add padding

    const root = d3.hierarchy(data);
    const treeLayout = d3.tree().size([width - 100, height - 100]);
    treeLayout(root);

    // Links (Arrows)
    svg.selectAll(".link")
      .data(root.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", d3.linkVertical()
                   .x(d => d.x)
                   .y(d => d.y))
      .style("stroke", "#aaa")
      .style("fill", "none");

    // Nodes (Circles)
    svg.selectAll(".node")
      .data(root.descendants())
      .enter()
      .append("circle")
      .attr("class", "node")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("r", d => 20 - d.depth * 5)  // Decrease radius based on depth
      .style("fill", "#4a90e2")
      .style("stroke", "black");

    // Node Labels (Move + Value + Best Move)
    svg.selectAll(".label")
      .data(root.descendants())
      .enter()
      .append("text")
      .attr("class", "label")
      .attr("x", d => d.x)
      .attr("y", d => d.y + 25) // Position slightly below the node
      .style("font-size", d => `${Math.max(7, 12 - d.depth*2)}px`)  // Decrease font size based on depth, with a minimum of 10px
      .style("fill", "black")  // Changed text color to black
      .style("text-anchor", "middle")
      .html(d => {
        // Display best move and value
        const move = `M: ${d.data.move !== null ? d.data.move : 'Root'}`;
        const value = `V: ${d.data.value}`;
        const bestMove = `B: ${d.data.best_move !== null ? d.data.best_move : '-'}`;
        return `${move}<tspan x="${d.x}" dy="1.2em">${value}</tspan><tspan x="${d.x}" dy="1.2em">${bestMove}</tspan>`;
      });
  }
</script>

<div class="svg-container">
  <svg bind:this={svgContainer}></svg>
</div>

<style>
  .svg-container {
    width: 100%;       /* Container should take full width */
    height: 500px;     /* Set a fixed height for the container */
    overflow: auto;    /* Enable scrolling */
    border: 1px solid #ccc;
    overflow-x: scroll;
    overflow-y: scroll;
  }

  svg {
    background-color: transparent;  /* Set background to transparent */
  }

  .node {
    stroke-width: 2px;
  }

  .label {
    font-weight: bold;
    font-family: Arial, sans-serif;
    pointer-events: none;  /* Ensure text doesn't interfere with interactions */
  }
</style>
