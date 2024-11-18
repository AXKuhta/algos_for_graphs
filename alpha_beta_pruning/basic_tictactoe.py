
import webbrowser

from bitmap import Bitmap

class BoardState:
	bitmap = None
	future = None
	past = None

	utility_o = None
	utility_x = None
	utility = None
	turn = 0

	def __init__(self, bitmap, past=None, turn=0, moved=""):
		self.bitmap = bitmap
		self.future = []
		self.past = past
		self.turn = turn
		self.moved = moved

	# Оценить полезность этого конкретного состояния
	# Возможны два сценария:
	# - Агент пытается максимизировать только свою полезность
	#   тогда сразу можно представить плохое поведение
	#   где он идёт к победе в сторонке
	#   и игнорирует другого игрока
	# - Агент пытается максимизировать/минимизировать общую полезность
	#   тогда он будет мешать другому игроку
	#
	# Путь o будет минимизатором, а x - максимизатором
	# utility = utility_x - utility_o
	#
	def estimate_utility(self):
		weights_x = {
			10: 	b"x..",
			10: 	b".x.",
			10: 	b"..x",
			100: 	b"xx.",
			100: 	b".xx",
			1000: 	b"xxx"
		}

		weights_o = {
			10: 	b"o..",
			10: 	b".o.",
			10: 	b"..o",
			100: 	b"oo.",
			100: 	b".oo",
			1000: 	b"ooo"
		}

		utility_x = 0
		utility_o = 0

		projections = []
		projections.extend(self.bitmap.rows())
		projections.extend(self.bitmap.cols())
		projections.extend(self.bitmap.pri_diag())
		projections.extend(self.bitmap.sec_diag())

		for k, v in weights_x.items():
			for projection in projections:
				if v in projection:
					utility_x += k

		for k, v in weights_o.items():
			for projection in projections:
				if v in projection:
					utility_o += k

		self.utility_x = utility_x
		self.utility_o = utility_o
		self.utility = utility_x - utility_o

	# Проверить, является ли состояние победным
	def test_winner(self):
		for row in self.bitmap.rows():
			if b"xxx" in row:
				return "x"
			if b"ooo" in row:
				return "o"

		for col in self.bitmap.cols():
			if b"xxx" in col:
				return "x"
			if b"ooo" in col:
				return "o"

		for pri in self.bitmap.pri_diag():
			if b"xxx" in pri:
				return "x"
			if b"ooo" in pri:
				return "o"

		for sec in self.bitmap.sec_diag():
			if b"xxx" in sec:
				return "x"
			if b"ooo" in sec:
				return "o"

		return ""

	def explore_(self, player):
		futures = []

		for i, v in enumerate(self.bitmap.bitmap):
			if v != ord("."):
				continue

			bitmap = self.bitmap.clone()
			bitmap.bitmap[i] = ord(player)
			future = BoardState(bitmap, self, self.turn + 1, player)

			futures.append(future)

		return futures

	# Сделать все возможные ходы
	# Вернёт массив допустимых будущих состояний
	def explore(self):
		winner = self.test_winner()

		if winner:
			self.estimate_utility()
			return []

		if self.turn == 0:
			self.future = self.explore_("x") + self.explore_("o")
		else:
			self.future = self.explore_("o" if self.moved == "x" else "x")

		if not self.future:
			self.estimate_utility()

		return self.future

	def html(self, depth=0, reachable=True):
		if depth > 5:
			return ""

		#if reachable:
		#	if self.turn & 1: # Ход o
		#		if self.utility_o < max(self.past.future, key=lambda x: x.utility_o).utility_o: # Подсмотреть в альтернативные вселенные
		#			reachable = False # Понятно, что o так не сходит - окрасить эту ветвь будущего красным

		class_lst = ["state"]

		if not reachable:
			class_lst.append("unreachable")

		nested = "<details>" + "".join([x.html(depth+1, reachable) for x in self.future]) + "</details>"
		classes = " ".join(class_lst)

		return f"<div class=\"{classes}\"><div>{self.bitmap}</div><div>utility: {self.utility:.3f}</div><div>{nested}</div></div>"
		#return f"<div class=\"{classes}\"><div>{self.bitmap}</div><div>utility x: {self.utility_x:.3f}</div><div>utility o: {self.utility_o:.3f}</div><div>{nested}</div></div>"

	def draw(self):
		with open("chart.html", "w") as f:
			f.write("<!DOCTYPE html>")
			f.write("<style>div { white-space: pre-wrap; font-family: monospace; font-size: 14px; }</style>")
			f.write("<style>.state { display: inline-block; margin: 2rem; padding: 2rem; border: 1px solid black; }</style>")
			f.write("<style>.unreachable { background-color: tomato; }</style>")
			f.write(self.html())

		webbrowser.open("chart.html")

	def __repr__(self):
		return f"BoardState(utility_x={self.utility_x}, utility_o={self.utility_o})"


init_bytes = 	b"..."\
		b"..."\
		b"..."

init_bm = Bitmap(init_bytes, 3, 3)
init = BoardState(init_bm, None)


# Пробежка по пространству состояний
# Держим состояния в очереди
def explore_states(init):
	pending = [init]

	while len(pending):
		state = pending.pop()
		options = state.explore()

		for option in options:
			pending.append(option)

# Поднять полезность
# o - минимизатор
# x - максимизатор
def hoist_utility(init):
	for option in init.future:
		if option.utility_x is None:
			hoist_utility(option)

	if init.moved == "o":
		init.utility = max([x.utility for x in init.future])
	elif init.moved == "x":
		init.utility = min([x.utility for x in init.future])
	else:
		pass # Готово

def play(loc):
	if not loc.future:
		print("Game over")
		return

	print("Make your move:")

	for i, s in enumerate(loc.future):
		print(f"=== {i} ===")
		print(s.bitmap)

	# Человек
	idx = int(input("> "))
	loc = loc.future[idx]

	# Компьютер
	if loc.moved == "x":
		loc = min(loc.future, key=lambda x: x.utility)
	elif loc.moved == "o":
		loc = max(loc.future, key=lambda x: x.utility)

	loc.draw()

	print("Computer makes a move:")
	print(loc.bitmap)
	input("Press enter")

	play(loc)

explore_states(init)
hoist_utility(init)
play(init)
