
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
		self.x_appetite = -99999
		self.o_appetite = +99999

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
			b"x...": 10,
			b".x..": 10,
			b"..x.": 10,
			b"...x": 10,
			b"xx..": 100,
			b".xx.": 100,
			b"..xx": 100,
			b"xxx.": 1000,
			b".xxx": 1000,
			b"xxxx": 10000
		}

		weights_o = {
			b"o...": 10,
			b".o..": 10,
			b"..o.": 10,
			b"...o": 10,
			b"oo..": 100,
			b".oo.": 100,
			b"..oo": 100,
			b"ooo.": 1000,
			b".ooo": 1000,
			b"oooo": 10000
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
				if k in projection:
					utility_x += v

		for k, v in weights_o.items():
			for projection in projections:
				if k in projection:
					utility_o += v

		self.utility_x = utility_x
		self.utility_o = utility_o
		self.utility = utility_x - utility_o

	# Проверить, является ли состояние победным
	def test_winner(self):
		for row in self.bitmap.rows():
			if b"xxxx" in row:
				return "x"
			if b"oooo" in row:
				return "o"

		for col in self.bitmap.cols():
			if b"xxxx" in col:
				return "x"
			if b"oooo" in col:
				return "o"

		for pri in self.bitmap.pri_diag():
			if b"xxxx" in pri:
				return "x"
			if b"oooo" in pri:
				return "o"

		for sec in self.bitmap.sec_diag():
			if b"xxxx" in sec:
				return "x"
			if b"oooo" in sec:
				return "o"

		return ""

	# Поставить крестик или нолик во всех возможных местах
	# Возвращает массив вселенных
	def explore_(self, player):
		futures = []

		for i, v in enumerate(self.bitmap.bitmap):
			if v != ord("."):
				continue

			bitmap = self.bitmap.clone()
			bitmap.bitmap[i] = ord(player)
			if i >= bitmap.w:
				bitmap.bitmap[i - bitmap.w] = ord(".")
			future = BoardState(bitmap, self, self.turn + 1, player)

			futures.append(future)

		return futures

	# Исследовать возможные ветки будущего и вытащить из каждой конечную полезность
	#
	# Не заходить в ветки где:
	# - полезность меньше некоторого порога если ходит x (x - максимизатор)
	# - полезность выше некоторого порока если ходит o (o - минимизатор)
	#
	# Пороги обновляются, когда x или o обнаружил более благоприятный для себя вариант
	#
	def explore(self, depth=0):
		winner = self.test_winner()

		# Кто-то победил или достигнута максимальная глубина?
		# Ранний выход
		if winner or depth >= 7:
			return []

		if self.turn == 0:
			self.future = self.explore_("x") + self.explore_("o")
		else:
			self.future = self.explore_("o" if self.moved == "x" else "x")

		# Оценить варианты будущего
		# Поиск в глубину
		for future in self.future:
			future.estimate_utility()
			moving = future.moved

			future.x_appetite = self.x_appetite
			future.o_appetite = self.o_appetite

			# Пропуск если будущее не соответствует аппетитам
			if moving == "x":
				if future.utility < self.x_appetite:
					continue
			elif moving == "o":
				if future.utility > self.o_appetite:
					continue
			else:
				assert 0

			# Спуск
			future.explore(depth+1)

			# Вернулись
			# Здесь мы должны обновить аппетиты
			if moving == "x":
				if future.utility >= self.x_appetite:
					self.x_appetite = future.utility
					self.utility = future.utility
			elif moving == "o":
				if future.utility <= self.o_appetite:
					self.o_appetite = future.utility
					self.utility = future.utility

		return self.future

	def nodes(self):
		return 1 + sum([x.nodes() for x in self.future])

	def leaves(self):
		return sum([x.leaves() for x in self.future]) or 1

	def html(self, depth=0, reachable=True):

		# o - минимизатор
		# x - максимизатор
		# Подсмотреть в альтернативные вселенные
		# Покрасить заведомо недостижимые ветки красным (при оптимальных игроках)
		if reachable:
			if self.moved == "x": # Ходил x
				if self.utility < max(self.past.future, key=lambda x: x.utility).utility:
					reachable = False
			elif self.moved == "o": # Ходил o
				if self.utility > min(self.past.future, key=lambda x: x.utility).utility:
					reachable = False

		class_lst = ["state"]

		if not reachable:
			class_lst.append("unreachable")

		nested = f"<details><summary>{self.leaves()} leaves</summary>" + "".join([x.html(depth+1, reachable) for x in self.future]) + "</details>"
		classes = " ".join(class_lst)

		return f"<div class=\"{classes}\"><div>{self.bitmap}</div><div>utility: {self.utility:.3f}</div><div>{nested}</div></div>"

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
