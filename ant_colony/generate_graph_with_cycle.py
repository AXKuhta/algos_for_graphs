
from random import randint

nodes = 50
edges = {}

#
# Сделать цикл
#
for i in range(nodes):
	a = i
	b = i+1

	edges[ a, b ] = 1

#
# Замкнуть цикл
#
edges[nodes, 0] = 2

#
# Наделать рандомных дополнительных ребер
#
# 50*49/2 - 50
for i in range(1000):
	while True:
		a = randint(0, nodes)
		b = randint(0, nodes)
		if (a, b) not in edges:
			edges[ a, b ] = randint(1, 30)
			break

print("Source	Target	Weight")

#
# Вывести
#
for (a, b), v in edges.items():
	print(f"{a}\t{b}\t{v}")
