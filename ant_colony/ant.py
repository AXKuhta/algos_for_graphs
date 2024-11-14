
from random import choice, choices, seed
import json
import sys

import matplotlib.pyplot as plt

seed(42)

#
# Настройки
#
settings = {
	"epochs": 1000,		# Количество эпох
	"stagnation": 50,	# Порог раннего выхода при стагнации (меньше - раньше)
	"alpha": 1.0,
	"beta": 1.0,
	"rho": 0.99		# Испарение феромона (больше - медленнее)
}

with open("settings.json") as f:
	settings.update(json.load(f))

epochs = settings["epochs"]
stagnation = settings["stagnation"]
alpha = settings["alpha"]
beta = settings["beta"]
rho = settings["rho"]

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
				tau = 0.1,
				nu = 1/w,
				a=a,
				b=b
			)

			edges[ a, b ] = edge

			a.connected.append( (b, edge) )

	#
	# Проверки на разумность:
	# - Есть ли ловушки?
	# - Есть ли абсолютно недостижимые ноды?
	#
	for node in nodes.values():
		assert len(node.connected) > 0, f"node {node} is a trap"

	reachable = set([b for a, b in edges])

	for node in nodes.values():
		assert node in reachable, f"node {node} is unreachable"

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

# Применить испарение
def apply_evaporation():
	for k, v in edges.items():
		v.tau *= rho

def run():
	if len(sys.argv) < 2:
		print("Usage: python3 ant.py 1000.txt")
		return

	load_from_file(sys.argv[1])

	# Вести историю стоимости найденых путей
	# И кумулятивного минимума стоимости за эпоху
	cost_log = []
	min_cost_x = []
	min_cost_y = []
	min_cost = None
	min_path = None

	# Главный цикл
	for i in range(epochs):
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

					if min_cost is None or ant.cost < min_cost:
						min_cost = ant.cost
						min_path = ant.hist
				else:
					assert 0

			pending = retained
			apply_evaporation()

		min_cost_x.append(i)
		min_cost_y.append(min_cost)

		# Нет изменений за последние эпохи - стагнация - ранний выход
		if i >= stagnation and len(set(min_cost_y[-stagnation:])) == 1:
			print("stagnated at", i)
			break

	if min_path:
		print("Final cost", min_cost)
		print("Final path", min_path)

		plt.figure(dpi=300)
		plt.title("Cost history")
		plt.xlabel("Epoch")
		plt.ylabel("Cumulative min cost")
		plt.plot(min_cost_x, min_cost_y)
		plt.show()
	else:
		print("Error: no cycle found")

run()
