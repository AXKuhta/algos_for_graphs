from queue import PriorityQueue
from ctypes import cdll

from bitmap import Bitmap

lib = cdll.LoadLibrary("./fast_board/lib.so")

class BoardState:
	bitmap = None
	future = None
	past = None

	utility_o = None
	utility_x = None
	utility = None
	winner = 0
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

	# Вторая версия функции оценки полезности
	# Менее читабельная и немного отличается поведением:
	# старая: x.x.... utility_x=20
	# новая:  x.x.... utility_x=120
	# Но работает быстрее
	def estimate_utility_v2(self):
		utility_x = 0
		utility_o = 0

		projections = []
		projections.extend(self.bitmap.rows())
		projections.extend(self.bitmap.cols())
		projections.extend(self.bitmap.pri_diag())
		projections.extend(self.bitmap.sec_diag())

		d = ord(".")
		s = ord(" ")
		x = ord("x")
		o = ord("o")

		for projection in projections:
			acc_d = 0
			acc_x = 0
			acc_o = 0
			acc_s = 0

			for push in projection[:4]:
				if push == s:
					acc_s += 1
				elif push == d:
					acc_d += 1
				elif push == x:
					acc_x += 1
				else:
					acc_o += 1

			if acc_s == 0:
				if acc_d == 3:
					if acc_x == 1:
						utility_x += 10
					elif acc_o == 1:
						utility_o += 10
				elif acc_d == 2:
					if acc_x == 2:
						utility_x += 100
					elif acc_o == 2:
						utility_o += 100
				elif acc_d == 1:
					if acc_x == 3:
						utility_x += 1000
					elif acc_o == 3:
						utility_o += 1000
				elif acc_d == 0:
					if acc_x == 4:
						utility_x += 10000
					elif acc_o == 4:
						utility_o += 10000

			for push, pop in zip(projection[4:], projection):
				#for i in range(len(projection) - 4):
				#	pop = projection[i]
				#	push = projection[i + 4]

				if push == s:
					acc_s += 1
				elif push == d:
					acc_d += 1
				elif push == x:
					acc_x += 1
				else:
					acc_o += 1

				if pop == s:
					acc_s -= 1
				elif pop == d:
					acc_d -= 1
				elif pop == x:
					acc_x -= 1
				else:
					acc_o -= 1

				if acc_s == 0:
					if acc_d == 3:
						if acc_x == 1:
							utility_x += 10
						elif acc_o == 1:
							utility_o += 10
					elif acc_d == 2:
						if acc_x == 2:
							utility_x += 100
						elif acc_o == 2:
							utility_o += 100
					elif acc_d == 1:
						if acc_x == 3:
							utility_x += 1000
						elif acc_o == 3:
							utility_o += 1000
					elif acc_d == 0:
						if acc_x == 4:
							utility_x += 10000
						elif acc_o == 4:
							utility_o += 10000

		self.utility_x = utility_x
		self.utility_o = utility_o
		self.utility = utility_x - utility_o

	# V3: внешняя оценочная функция на C
	def estimate_utility_v3(self):
		utility_x = bytes(4) # Память для возвратных значений
		utility_o = bytes(4) # не надо так делать - bytes вообще-то read-only
		winner = bytes(1)

		lib.estimate_utility_v2c(
			bytes(self.bitmap.bitmap),
			self.bitmap.w,
			self.bitmap.h,
			4,
			utility_x,
			utility_o,
			winner
		)

		self.utility_x = int.from_bytes(utility_x, "little")
		self.utility_o = int.from_bytes(utility_o, "little")
		self.utility = self.utility_x - self.utility_o
		self.base_utility = self.utility
		self.winner = winner[0]

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

		# Кто-то победил или достигнута максимальная глубина?
		# Ранний выход
		if self.winner or depth >= 3:
			return []

		assert self.moved, "I don't know whose turn it is"

		self.future = self.explore_("o" if self.moved == "x" else "x")

		prio = PriorityQueue()

		for future in self.future:
			future.estimate_utility_v3()
			prio.put(future)

		# Оценить варианты будущего
		# Поиск в глубину
		while not prio.empty():
			future = prio.get()

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

	# Для очереди с приоритетом
	def __lt__(self, other):
		if self.moved == "x":
			return self.utility > other.utility
		else:
			return self.utility < other.utility

bm_init = 	b"       "\
		b"       "\
		b"       "\
		b"       "\
		b". .    "\
		b"x.x...."\

bm = Bitmap(bm_init, 7, 6)
state = BoardState(bm)
