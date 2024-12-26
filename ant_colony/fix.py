
#
# Нода
#
class Node:
	def __init__(self, name):
		self.connected = []
		self.name = name

	def __repr__(self):
		return f"Node({self.name})"

nodes = {}

#
# Ребро
#
class Edge:
	a = None
	b = None
	cost = 0

	def __init__(self, cost, a, b):
		self.cost = cost
		self.a = a
		self.b = b

	def __iter__(self):
		yield self.nu
		yield self.tau

	def __repr__(self):
		return f"{self.a.name} --{self.cost}--> {self.b.name}"

edges = {}

#
# Загрузка графа
#
def load_from_file(filename):
	with open(filename) as f:
		for line in f:
			break

		for line in f:
			a, b, w = line.strip().split("\t")
			w = int(w)

			if a not in nodes:
				nodes[a] = Node(a)
			a = nodes[a]

			if b not in nodes:
				nodes[b] = Node(b)
			b = nodes[b]

			edge = Edge(
				cost = w,
				a=a,
				b=b
			)

			# Здесь сделать граф полносвязным
			# превратив ребро в set
			edges[ frozenset( (a, b) ) ] = edge

			a.connected.append( (b, edge) )

load_from_file("1000.txt")

n = len(nodes)
print("G has", n, "nodes")
print("G has", len(edges), "edges")

# Делаем полносвязный граф
edges_fc = {}

# Пробежка по нижнему треугольнику матрицы смежности
nodelist = list(nodes.values())

for i, a in enumerate(nodelist):
	for b in nodelist[:i]:
		edges_fc[ frozenset( (a, b) ) ] = 1

print("Fully connected G has", len(edges_fc), "edges")

# Возьмем набор рёбер, которые разрешено убирать
removable = set(edges_fc.keys()) - set(edges.keys())

# Табличка det
degree_of_incidence = { node: n - 1 for node in nodes.values() }

remove = set()

for k in removable:
	a, b = k

	if degree_of_incidence[a] + degree_of_incidence[b] >= n + 2:
		degree_of_incidence[a] -= 1
		degree_of_incidence[b] -= 1
		remove.add(k)

retain = set(edges_fc.keys()) - remove

print("Fixed G has", len(retain), "edges")

# Сохранить граф
# Должен быть по крайней мере гамильтонов цикл со стоииостью 177572
with open("1000_fix.txt", "w") as f:
	f.write("Source\tTarget\tWeight\r\n")

	for v in edges.values():
		f.write(f"{v.a.name}\t{v.b.name}\t{v.cost}\r\n")

	for k in retain - set(edges.values()):
		a, b = k
		f.write(f"{a.name}\t{b.name}\t999\r\n")
