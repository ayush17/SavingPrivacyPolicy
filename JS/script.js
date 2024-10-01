d3.json("inferences.json").then(function (data) {
    const sets = data.data;

    sets.forEach((set, index) => {
        const initialWidth = window.innerWidth;
        const initialHeight = window.innerHeight - 50;

        const container = d3.select("#graphs")
            .append("div")
            .attr("class", "graph-container");

        container.append("div")
            .attr("class", "graph-title")
            .text(`Graph ${index + 1}`);

        const svgContainer = container.append("div")
            .attr("class", "svg-container")
            .append("svg")
            .attr("width", initialWidth)
            .attr("height", initialHeight)
            .append("g");

        const nodes = [];
        const links = [];

        set.inferences.forEach(inference => {
            const root = inference.root[0];
            nodes.push({ id: root, isRoot: true });
            inference.children.forEach(child => {
                nodes.push({ id: child, isRoot: false });
                links.push({ source: root, target: child });
            });
        });

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink().id(d => d.id).distance(80)) // Adjust distance for better spacing
            .force("charge", d3.forceManyBody().strength(-60)) // Adjust charge for spacing
            .force("center", d3.forceCenter(initialWidth / 2, initialHeight / 2))
            .on("tick", updateGraphSize);

        const link = svgContainer.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke", "#999")
            .style("stroke-opacity", 0.6);

        const node = svgContainer.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(nodes)
            .enter().append("g")
            .attr("class", "node");

        node.append("circle")
            .attr("r", d => d.isRoot ? 12 : 8)
            .attr("fill", d => d.isRoot ? "red" : "green");

        node.append("text")
            .attr("dx", 10)
            .attr("dy", ".35em")
            .text(d => d.id);

        simulation.nodes(nodes);
        simulation.force("link").links(links);

        function updateGraphSize() {
            const bounds = {
                minX: d3.min(nodes, d => d.x),
                maxX: d3.max(nodes, d => d.x),
                minY: d3.min(nodes, d => d.y),
                maxY: d3.max(nodes, d => d.y)
            };
            const newWidth = Math.max(initialWidth, bounds.maxX - bounds.minX + 100); // Add padding
            const newHeight = Math.max(initialHeight, bounds.maxY - bounds.minY + 100); // Add padding

            d3.select(container.node().querySelector("svg"))
                .attr("width", newWidth)
                .attr("height", newHeight);

            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        }
    });
}).catch(error => {
    console.error("Error loading the JSON data: ", error);
});
