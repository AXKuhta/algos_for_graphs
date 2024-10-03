import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()

with open("edgelist_simple.txt") as f:
	for line in f:
		a, b, w = line.strip().split(",")
		w = int(w)

		G.add_edge(a, b, weight=w)
		G.add_edge(b, a, weight=w)

cycle = nx.algorithms.approximation.greedy_tsp(G, source="a")
#print(nx.algorithms.approximation.traveling_salesman_problem(G))

#pos = nx.spring_layout(G)
pos = nx.spiral_layout(G)

edge_list = list(nx.utils.pairwise(cycle))


print(edge_list)

labels = {}

for u, v in G.edges:
	nx.set_edge_attributes(G, {(u, v): {"color": "black"}})
	nx.set_edge_attributes(G, {(u, v): {"width": 1}})

for i, (u, v) in enumerate(edge_list):
	nx.set_edge_attributes(G, {(u, v): {"color": "red"}})
	labels[(u, v)] = i

plt.figure(figsize=[16, 9], dpi=300)

nx.draw_networkx(
    G,
    pos,
    edge_color=[G.get_edge_data(u, v)["color"] for u, v in G.edges],
    node_color="white", # Node color
    edgecolors="black"  # Node edge color
)


nx.draw_networkx_edge_labels(
	G,
	pos,
	labels,
)

plt.show()
