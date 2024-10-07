import networkx as nx
import matplotlib.pyplot as plt


data = [
    {"root": ["Living situation"], "children": ["rent ain't cheap", "solo flat hunt"]},
    {
        "root": ["Location"],
        "children": [
            "underground live music spots",
            "parks",
            "open mic nights",
            "small venue gigs",
        ],
    },
    {
        "root": ["Occupation/Age inference"],
        "children": [
            "reviews and gigs",
            "Music critics",
            "Spotify’s top 100",
            "date nights",
            "reviewing",
        ],
    },
    {"root": ["Age inference"], "children": ["adulting", "growing your own veggies"]},
    {"root": ["Age group"], "children": ["🤷‍♂️", "😀", "😂"]},
    {"root": ["Age indication"], "children": ["Lol"]},
]

G = nx.DiGraph()

for category in data:
    root = category["root"][0]  # Get the root
    G.add_node(root)  # Add root node
    for child in category["children"]:
        G.add_node(child)  # Add child node
        G.add_edge(root, child)  # Create edge from root to child

plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)  # positions for all nodes

root_nodes = [category["root"][0] for category in data]
child_nodes = [child for category in data for child in category["children"]]

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=root_nodes,
    node_size=4000,
    node_color="lightblue",
    label="Root Nodes",
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=child_nodes,
    node_size=2000,
    node_color="lightgreen",
    label="Child Nodes",
)

nx.draw_networkx_edges(G, pos)


nx.draw_networkx_labels(
    G, pos, labels={node: node for node in root_nodes}, font_size=12, font_weight="bold"
)

# Draw labels for child nodes (italic)
for node in child_nodes:
    plt.text(
        pos[node][0],
        pos[node][1],
        node,
        fontsize=10,
        fontstyle="italic",
        ha="center",
        va="center",
    )

plt.title("Semantic Knowledge Graph")
plt.axis("off")  # Hide axes
plt.show()
