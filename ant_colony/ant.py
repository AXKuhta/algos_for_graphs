from random import choices

#
# Настройки
#
p = 0.9		# Испарение феромона

#
# Нода
#
class node:
	def __init__(self, name):
		self.connected = []
		self.name = name

	def __repr__(self):
		return f"node({self.name})"

#
# Тау и ню
#
all_tau = {}
all_nu = {}
nodes = {}

#
# Загрузка графа
#
with open("edgelist.txt") as f:
	for line in f:
		a, b, w = line.strip().split(",")
		w = int(w)

		if a not in nodes:
			nodes[a] = node(a)
		a = nodes[a]

		if b not in nodes:
			nodes[b] = node(b)
		b = nodes[b]

		all_tau[ a, b ] = 0.1
		all_nu[ a, b ] = 1/w

		a.connected.append(b)

set_nodes = set(nodes.values())

solutions = []

#
# Муравей
#
class ant:
	def __init__(self, loc):
		self.seen = set()
		self.hist = []
		self.loc = loc

	def advance(self):
		options = []
		weights = []

		for dst in self.loc.connected:
			a = self.loc
			b = dst

			nu = all_nu[a, b]
			tau = all_tau[a, b]

			options.append(dst)
			weights.append(nu*tau)

		#w_sum = sum(weights)
		#weights = [x/w_sum for x in weights]

		where, = choices(options, weights)
		self.hist.append( (self.loc, where) )

		self.loc = where
		self.seen.add(self.loc)

		if self.seen == set_nodes:
			self.activate_trail()
			solutions.append(len(self.hist))
			return 0

		return 1

	def activate_trail(self):
		self.hist.reverse()

		for i, edge in enumerate(self.hist):
			all_tau[edge] += 1 * (p**i)

# Начальная (и конечная) точка
init = nodes["a"]

# Муравьи
ants = [ant(init) for i in range(10)]

for i in range(1000):
	ants_ = []

	# Шагнуть каждым муравьём
	# Вернулись - убрать старого, создать нового
	for x in ants:
		if x.advance():
			ants_.append(x)
		else:
			ants_.append( ant(init) )

	# Применить испарение
	for k in all_tau:
		all_tau[k] = all_tau[k] * p

	ants = ants_

	if not len(ants):
		break

import matplotlib.pyplot as plt

plt.figure()
plt.plot(solutions)
plt.show()
