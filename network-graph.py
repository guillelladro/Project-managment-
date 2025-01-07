
import networkx as nx
import matplotlib.pyplot as plt

# Define the tasks and dependencies for the CPM diagram
tasks = [
    ("Requirement Gathering", "WBS Development"),
    ("WBS Development", "Backend Development"),
    ("Backend Development", "Frontend Development"),
    ("Frontend Development", "Testing"),
    ("Testing", "Deployment"),
]

# Define parallel activities
parallel_activities = [
    ("API integration", "Backend Development"),
    ("Database design", "Backend Development"),
    ("UI/UX development", "Frontend Development"),
    ("Accessibility features", "Frontend Development"),
    ("Unit testing", "Testing"),
    ("Integration testing", "Testing"),
]

# Create a directed graph
G = nx.DiGraph()

# Add edges for sequential dependencies
G.add_edges_from(tasks)

# Add edges for parallel activities
G.add_edges_from(parallel_activities)

# Define node positions for better visualization
pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20)

# Highlight the critical path (longest path in terms of dependencies)
critical_path = ["Requirement Gathering", "WBS Development", "Backend Development", "Frontend Development", "Testing", "Deployment"]
critical_edges = [(critical_path[i], critical_path[i + 1]) for i in range(len(critical_path) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=critical_edges, edge_color="red", width=2)

# Add title and legend
plt.title("CPM Network Diagram", fontsize=16)
plt.legend(["Critical Path (red)", "Other Paths"], loc="upper left", fontsize=10)

plt.show()
