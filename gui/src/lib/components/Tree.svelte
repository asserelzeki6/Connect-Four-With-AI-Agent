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

    const width = 1000;  // Increased width for better spacing
    const height = 600;

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
      .attr("r", 20)
      .style("fill", "#4a90e2")
      .style("stroke", "black");

    // Node Labels (Move + Best Move)
    svg.selectAll(".label")
      .data(root.descendants())
      .enter()
      .append("text")
      .attr("class", "label")
      .attr("x", d => d.x - 10)
      .attr("y", d => d.y + 5)
      .text(d => (d.depth === 0 ? `Best: ${d.data.best_move}` : `Move: ${d.data.move}`))
      .style("font-size", "12px")
      .style("fill", "white")
      .style("text-anchor", "middle");
  }
</script>

<svg bind:this={svgContainer}></svg>

<style>
  svg {
    border: 1px solid #ccc;
    width: 100%;
    height: 100%;
  }
  .node {
    stroke-width: 2px;
  }
  .label {
    font-weight: bold;
  }
</style>
