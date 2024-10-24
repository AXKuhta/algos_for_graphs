
from random import choice, choices

import matplotlib.pyplot as plt
import networkx as nx

#
# Настройки
#
alpha = 1.0
beta = 1.0
rho = 0.9		# Испарение феромона


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
# Тау и ню
#
class Edge:
	cost = 0
	tau = 0
	nu = 0

	def __init__(self, cost, tau, nu):
		self.cost = cost
		self.tau = tau
		self.nu = nu

	def __iter__(self):
		yield self.nu
		yield self.tau

edges = {}

#
# Отрисовка графа
#
def display(edges):
	G = nx.DiGraph()

	labels_w = {}
	labels_i = {}

	for k, v in edges.items():
		a, b = k

		G.add_edge(a.name, b.name)

		labels_w[ (a.name, b.name) ] = f"{v.cost}"
		labels_i[ (a.name, b.name) ] = f"{v.tau:.2f}"

	pos = nx.circular_layout(G)

	plt.figure(figsize=[16, 9], dpi=300)

	nx.draw_networkx(
		G,
		pos,
		node_color="white", # Node colors
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
		label_pos = 0.3,
		rotate=False,
		bbox={}
	)

	plt.show()


#
# Загрузка графа
#
with open("synthetic.txt") as f:
	#for line in f:
	#	break

	for line in f:
		a, b, w = line.strip().split(",")
		w = int(w)

		if a not in nodes:
			nodes[a] = Node(a)
		a = nodes[a]

		if b not in nodes:
			nodes[b] = Node(b)
		b = nodes[b]

		edge = Edge(
			cost = w,
			tau = 0.1,
			nu = 1/w
		)

		edges[ a, b ] = edge

		a.connected.append( (b, edge) )

#
# Что от нас требуется:
# - Мы муравей
# - Надо построить план
#   Это будет цикл
#
# - План выполняется
#   Все tau обновляются
# - Застряли
#   Умираем
#

#
# Какие у нас будут операции:
# - Доставание рандомной ноды
# - Получение набора соседей
# - Вычет посещенных мест
# - Сортировка по весам
#
# Данные шаги выполняются за n
# Путь не нашёлся, всё, кирдык
#

#
# Муравей
#
class Ant:
	def __init__(self, loc):
		self.seen = set()
		self.hist = []
		self.cost = 0
		self.init = loc
		self.loc = loc

	def advance(self):
		options = []
		weights = []

		self.seen.add(self.loc)

		for dst, edge in self.loc.connected:
			if dst in self.seen:
				continue

			nu, tau = edge

			options.append( (dst, edge) )
			weights.append( tau**alpha * nu**beta )

		if not options:
			if len(self.seen) != len(nodes):
				return "stuck"

			fin_edge = None

			for dst, edge in self.loc.connected:
				if dst == self.init:
					fin_edge = edge
					break

			if not fin_edge:
				return "stuck"

			self.cost += fin_edge.cost
			self.update_tau()
			return "fin"

		where, = choices(options, weights)
		dst, edge = where

		self.cost += edge.cost
		self.loc = dst

		self.hist.append(edge)

		return "continue"

	def update_tau(self):
		for edge in self.hist:
			edge.tau += 1/self.cost


cost = []
stuck = 0

def apply_evaporation():
	for k, v in edges.items():
		v.tau *= 0.9

for i in range(100):
	pending = [Ant(init) for init in nodes.values()]

	# Ходим
	while pending:
		retained = []

		for ant in pending:
			status = ant.advance()
			if status == "continue":
				retained.append(ant)
			elif status == "stuck":
				pass
			elif status == "fin":
				cost.append(ant.cost)
			else:
				assert 0

		pending = retained
		apply_evaporation()

print("Final cost", ant.cost)
plt.plot(cost)
plt.show()

#display(edges)
