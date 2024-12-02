<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let tree = null;
  let svgContainer;

  onMount(() => {
    if (tree) {
      drawTree(tree);
    }
  });

  function drawTree(data) {
    d3.select(svgContainer).selectAll("*").remove();  // Clear previous content

    // Set dimensions based on screen size
    const maxDepth = d3.max(d3.hierarchy(data).descendants(), d => d.depth);
    const numNodesAtMaxDepth = Math.pow(7, maxDepth - 1);  // Number of nodes at maximum depth
    const width = numNodesAtMaxDepth*80 ;
    const height = window.innerHeight * 0.8;

    const svg = d3.select(svgContainer)
                  .attr("width", width)
                  .attr("height", height)
                  .attr("viewBox", `0 0 ${width} ${height}`)
                  .append("g")
                  .attr("transform", `translate(${width / 10}, 50)`);

    // Calculate maximum depth of the tree
    const horizontalSpacing = width / (Math.log2(numNodesAtMaxDepth) * 7);  // Logarithmic scaling

    const root = d3.hierarchy(data);
    const treeLayout = d3.tree()
                         .size([width * 0.8, height * 0.7])
                         .separation((a, b) => (a.parent === b.parent ? 1.5 + a.depth / 3 : 2.5 + a.depth / 3));

    treeLayout(root);

    // Draw links
    svg.selectAll(".link")
      .data(root.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", d3.linkVertical()
                   .x(d => d.x)
                   .y(d => d.y))
      .style("stroke", "white")
      .style("fill", "none");

    // Draw nodes and shapes
    const nodes = svg.selectAll(".node")
      .data(root.descendants())
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", d => `translate(${d.x}, ${d.y})`);

    nodes.each(function(d) {
      const nodeGroup = d3.select(this);
      const { type, player, best_move, children } = d.data;

      if (type === 'Chance') {
        nodeGroup.append("circle")
          .attr("r", 30)
          .style("fill", "#4a90e2")
          .style("stroke", "black");
      } else if (type === 'Root') {
         if (player === 'y'){
          nodeGroup.append("polygon")
          .attr("points", "0,45 45,-45 -45,-45")  // Increased triangle size
          .style("fill", "yellow")
          .style("stroke", "black");
         }else{
          nodeGroup.append("polygon")
          .attr("points", "0,-45 45,45 -45,45")  // Increased triangle size
          .style("fill", "red")
          .style("stroke", "black");
         }
      }else if (!children.length || best_move === null) {
        nodeGroup.append("rect")
          .attr("width", 80)
          .attr("height", 50)
          .attr("x", -40)
          .attr("y", -25)
          .style("fill", "green")
          .style("stroke", "black");
      } else if (player === 'y') {
        nodeGroup.append("polygon")
          .attr("points", "0,-45 45,45 -45,45")  // Increased triangle size
          .style("fill", "red")
          .style("stroke", "black");
      } else if (player === 'r') {
        nodeGroup.append("polygon")
          .attr("points", "0,45 45,-45 -45,-45")  // Increased triangle size
          .style("fill", "yellow")
          .style("stroke", "black");
      } 
    });

    // Add labels inside nodes
    nodes.append("text")
    .attr("class", "label")
    .attr("dy", "0.3em")
    .style("font-size", "10px")
    .style("fill", "black")
    .style("text-anchor", "middle")
    .selectAll("tspan")  // Add tspan for vertical alignment
    .data(d => {
      const { move, utility, best_move } = d.data;
      const parts = [
        move !== null ? `M: ${move}` : null,
        utility !== null ? `V: ${utility}` : null,
        best_move !== null ? `B: ${best_move}` : null
      ].filter(Boolean);  // Remove null values
      return parts;
    })
    .enter()
    .append("tspan")
    .attr("x", 0)
    .attr("dy", (d, i) => i * 12)  // Vertical spacing between lines
    .text(d => d);

  }
</script>

<div class="svg-container">
  <svg bind:this={svgContainer}></svg>
</div>

<style>
  .svg-container {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    overflow-x: auto;
    overflow-y: auto;
    position: relative;

     /* white-space: nowrap;   */
    /* border: 1px solid #ccc; */
  }

  .label {
    font-family: Arial, sans-serif;
    white-space: pre;  /* Preserve line breaks */
  }
</style>
