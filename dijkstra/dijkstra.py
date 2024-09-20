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

with open("edgelist.txt") as file:
	for line in file:
		a, b, weight = [ int(v) for v in line.strip().split(",") ]

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

weights = {
	"1,2": 10,
	"1,3": 40,
	"2,3": 10
}

a = node("1")
b = node("2")
c = node("3")

a.connected.append(b)
a.connected.append(c)
b.connected.append(c)

walk(a, c)
