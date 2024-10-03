from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()

with open("edgelist.txt") as f:
	for line in f:
		a, b, w = line.strip().split(",")
		w = int(w)

		G.add_edge(a, b, weight=w)
		#G.add_edge(b, a, weight=w)

#
# Make a complete graph by adding cost 9999 edges
# but but but...
#
# Suppose this is a sparse graph
# 1000 nodes
# 10 edges
#
# Padding it out would be 1000! - 10 extra edges
# ...not going to happen
#
extra_edges = []

for u, v in permutations(G.nodes, 2):
	if not (u, v) in G.edges:
		extra_edges.append( (u, v, 9999) )

G.add_weighted_edges_from(extra_edges)

#cycle = nx.algorithms.approximation.greedy_tsp(G, source="a")
cycle = nx.algorithms.approximation.simulated_annealing_tsp(G, "greedy")
edge_list = list(nx.utils.pairwise(cycle))

#pos = nx.random_layout(G)
#pos = nx.spring_layout(G)
#pos = nx.spiral_layout(G)
pos = nx.circular_layout(G)

print(edge_list)

labels_w = {}
labels_i = {}

for u, v in G.edges:
	weight = G.get_edge_data(u, v)["weight"]
	if weight < 9999:
		nx.set_edge_attributes(G, {(u, v): {"color": "black"}})
		labels_w[(u, v)] = f"{weight}"
	else:
		nx.set_edge_attributes(G, {(u, v): {"color": "none"}})
		labels_w[(u, v)] = ""

for i, (u, v) in enumerate(edge_list):
	nx.set_edge_attributes(G, {(u, v): {"color": "red"}})
	labels_i[(u, v)] = f"{i}"

plt.figure(figsize=[16, 9], dpi=300)
plt.title(cycle)

nx.draw_networkx(
    G,
    pos,
    edge_color=[G.get_edge_data(u, v)["color"] for u, v in G.edges],
    node_color="white", # Node color
    edgecolors="black",  # Node edge color
	connectionstyle="arc3,rad=0.05"
)


nx.draw_networkx_edge_labels(
	G,
	pos,
	labels_w,
	connectionstyle="arc3,rad=0.05",
	font_size=5
)

nx.draw_networkx_edge_labels(
	G,
	pos,
	labels_i,
	connectionstyle="arc3,rad=0.05",
	font_color="white",
	label_pos = 0.4,
	rotate=False,
	bbox={}
)

plt.show()
