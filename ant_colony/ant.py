
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
class node:
	def __init__(self, name):
		self.connected = []
		self.name = name

	def __repr__(self):
		return f"node({self.name})"

nodes = {}

#
# Ребро
# Тау и ню
#
class edge:
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
with open("edgelist_simple.txt") as f:
	for line in f:
		a, b, w = line.strip().split(",")
		w = int(w)

		if a not in nodes:
			nodes[a] = node(a)
		a = nodes[a]

		if b not in nodes:
			nodes[b] = node(b)
		b = nodes[b]

		edges[ a, b ] = edge(
			cost = w,
			tau = 0.1,
			nu = 1/w
		)

		#a.connected.append( ( b, edges[ a, b ] ) )
		#a.connected[b] = edges[ a, b ]
		a.connected.append(b)

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
		self.edges = []
		self.hist = []
		self.cost = 0
		self.init = loc
		self.loc = loc

	def advance(self):
		options = []
		weights = []

		self.hist.append(self.loc)

		avail = set( self.loc.connected ) - set( self.hist )

		if not avail:
			if len(self.hist) != len(nodes):
				return "stuck"
			self.finish()
			return "fin"

		for dst in avail:
			k = (self.loc, dst)
			edge = edges[k]
			nu, tau = edge

			options.append( (dst, edge) )
			weights.append( tau**alpha * nu**beta )

		#w_sum = sum(weights)
		#weights = [x/w_sum for x in weights]

		where, = choices(options, weights)
		dst, edge = where

		self.cost += edge.cost
		self.loc = dst

		self.edges.append(edge)

		return "continue"

	def finish(self):
		assert self.init in self.loc.connected
		k = (self.loc, self.init)
		self.cost += edges[k].cost
		self.update_tau()

	def update_tau(self):
		for edge in self.edges:
			edge.tau += 1/self.cost


init = nodes["a"]
cost = []
stuck = 0

def apply_evaporation():
	for k, v in edges.items():
		v.tau *= 0.9

# Запускаем муравья
for i in range(1000):
	init = choice(list(nodes.values()))
	ant = Ant(init)
	while True:
		status = ant.advance()
		if status == "continue":
			pass
		elif status == "stuck":
			stuck += 1
			break
		elif status == "fin":
			cost.append(ant.cost)
			break
		else:
			assert 0

	apply_evaporation()

print(ant.hist)

print("Ants stuck", stuck)
plt.plot(cost)
plt.show()

display(edges)
