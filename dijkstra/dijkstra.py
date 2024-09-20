from queue import PriorityQueue

class node:
	name = ""
	cost = 9999
	seen = False
	back = None

	def __init__(self, name):
		self.connected = []
		self.name = name
		pass

	def __gt__(self, other):
		return self.cost > other.cost

	def __str__(self):
		return f"Node(name={self.name}, cost={self.cost})"

def walk(init, target):
	queue = PriorityQueue() # Маленькие первыми
	queue.put(init)

	init.cost = 0

	# Перебираем соседей
	# обновляем стоимость
	# заполняем очередь
	while not queue.empty():
		loc = queue.get()
		loc.seen = True

		print(f"In {loc}")

		for dst in loc.connected:
			if dst.seen:
				continue

			linkage_key = f"{loc.name},{dst.name}"
			cost_from_here = loc.cost + weights[linkage_key]

			if cost_from_here < dst.cost:
				dst.cost = cost_from_here
				dst.back = loc

			print(f"Establish that {dst}")

			queue.put(dst)

	# Пробегаемся от цели к началу
	hist = []
	loc = target

	while True:
		hist.append(loc.name)
		if loc.back:
			loc = loc.back
		else:
			break

	hist.reverse()

	print(f"Path from {init.name} to {target.name} costs {target.cost}: {hist}")

weights = {}
nodes = {}

with open("edgelist.txt") as file:
	for line in file:
		a, b, weight = [ int(v) for v in line.strip().split(",") ]
		weights[ f"{a},{b}" ] = weight

		if a not in nodes:
			nodes[a] = node(f"{a}")
		a = nodes[a]

		if b not in nodes:
			nodes[b] = node(f"{b}")
		b = nodes[b]

		a.connected.append(b)

start = nodes[1]
target = nodes[9]

walk(start, target)
