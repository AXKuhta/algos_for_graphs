from bitmap import Bitmap

class BoardState:
	bitmap = None
	future = None
	past = None

	utility_o = None
	utility_x = None
	turn = 0

	def __init__(self, bitmap, past, turn=0):
		self.bitmap = bitmap
		self.future = []
		self.past = past
		self.turn = turn

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

	# Сделать все возможные ходы
	# Вернёт массив допустимых будущих состояний
	def explore(self):
		winner = self.test_winner()

		if winner:
			self.utility_o = 1/self.turn if winner == "o" else 0
			self.utility_x = 1/self.turn if winner == "x" else 0
			#print("Branch terminated in", score)
			#print(self.bitmap)
			return []

		for i, v in enumerate(self.bitmap.bitmap):
			if v != ord("."):
				continue

			player = "x" if self.turn & 1 else "o"

			bitmap = self.bitmap.clone()
			bitmap.bitmap[i] = ord(player)
			future = BoardState(bitmap, self, self.turn + 1)

			self.future.append(future)

		return self.future

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
# Больше победных веток - выше полезность
def hoist_utility(init):
	for option in init.future:
		if option.utility_x is None:
			hoist_utility(option)

	init.utility_x = sum([x.utility_x for x in init.future])
	init.utility_o = sum([x.utility_o for x in init.future])

explore_states(init)
hoist_utility(init)
