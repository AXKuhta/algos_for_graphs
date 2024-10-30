from bitmap import Bitmap

class board_state:
	bitmap = None
	future = None
	past = None

	utility = None
	turn = ""

	def __init__(self, bitmap, past, turn):
		self.bitmap = bitmap
		self.future = []
		self.past = past
		self.turn = turn

	# Проверить, является ли состояние победным
	def test_game_over(self):
		for row in self.bitmap.rows():
			if b"xxx" in row:
				return +1
			if b"ooo" in row:
				return -1

		for col in self.bitmap.cols():
			if b"xxx" in col:
				return +1
			if b"ooo" in col:
				return -1

		for pri in self.bitmap.pri_diag():
			if b"xxx" in pri:
				return +1
			if b"ooo" in pri:
				return -1

		for sec in self.bitmap.sec_diag():
			if b"xxx" in sec:
				return +1
			if b"ooo" in sec:
				return -1

		return 0

	# Сделать все возможные ходы
	# Вернёт массив допустимых будущих состояний
	def explore(self):
		score = self.test_game_over()

		if score:
			print("Branch terminated in", score)
			return []

		for i, v in enumerate(self.bitmap.bitmap):
			if v != ord("."):
				continue

			bitmap = self.bitmap.clone()
			bitmap.bitmap[i] = ord(self.turn)
			future = board_state(bitmap, self, "x" if self.turn == "o" else "o")

			self.future.append(future)

		return self.future


init_bytes = 	b"..."\
		b"..."\
		b"..."

init_bm = Bitmap(init_bytes, 3, 3)

# Пробежка по пространству состояний
# Держим состояния в очереди
init = board_state(init_bm, None, "o")

pending = [init]

while len(pending):
	state = pending.pop()
	options = state.explore()

	for option in options:
		pending.append(option)
