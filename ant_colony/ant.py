
from random import choice, choices

import matplotlib.pyplot as plt
import networkx as nx

#
# Настройки
#
alpha = 1.0
beta = 1.0
rho = 0.99		# Испарение феромона (больше - медленнее)


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
	a = None
	b = None

	def __init__(self, cost, tau, nu, a, b):
		self.cost = cost
		self.tau = tau
		self.nu = nu
		self.a = a
		self.b = b

	def __iter__(self):
		yield self.nu
		yield self.tau

	def __repr__(self):
		return f"{self.a.name} -{self.cost}-> {self.b.name}"

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
			nu = 1/w,
			a=a,
			b=b
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

			self.hist.append(fin_edge)
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

# Вести историю стоимости найденых путей
# И кумулятивного минимума стоимости
cost_log = []
min_cost_log = []
min_cost = 9999
min_path = None

# Применить испарение
def apply_evaporation():
	for k, v in edges.items():
		v.tau *= rho

# Главный цикл
# Макс. 1000 перезапусков
for i in range(1000):
	pending = [Ant(init) for init in nodes.values()] # Поставить муравья в каждую ноду

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
				cost_log.append(ant.cost)

				if ant.cost < min_cost:
					min_cost = ant.cost
					min_path = ant.hist

				min_cost_log.append(min_cost)
			else:
				assert 0

		pending = retained
		apply_evaporation()

	# Нет изменения в стоимости последних 500 муравьёв - стагнация - ранний выход
	if len(set(min_cost_log[-500:])) == 1:
		print("stagnated at", i)
		break

print("Final cost", min_cost)
print("Final path", min_path)

plt.title("Total shortest path")
plt.xlabel("Ant number")
plt.ylabel("Cumulative min cost")
plt.plot(min_cost_log)
plt.show()

#display(edges)
