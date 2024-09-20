import networkx as nx
import numpy as np

edgelist = np.loadtxt("edgelist.txt", delimiter=",", dtype=int)
G = nx.Graph()

for a, b, w in edgelist:
	G.add_edge(a, b, weight=w)

for a, dst in nx.shortest_path_length(G, weight="weight"):
	print(a, dst)

print("1 to 9:")
print( nx.shortest_path(G,1,9, weight="weight") )
