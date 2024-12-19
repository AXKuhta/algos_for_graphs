from connect4_core import BoardState, lib

# Крестики нолики 20x20 отличаются от четырех в ряд:
# - оценочной функцией
#   нужно 5 в ряд
# - функцией перебора допустимых будущих
#   не нужно открывать новых позиций
#   т.к. все позиции открыты сразу
#   +нужно создавать TTTBoardState
#
# Класс TTTBoardState переопределяет эти функции
#
class TTTBoardState(BoardState):
	# Поставить крестик или нолик во всех возможных местах
	# Возвращает массив вселенных
	def explore_(self, player):
		futures = []

		for i, v in enumerate(self.bitmap.bitmap):
			if v != ord("."):
				continue

			bitmap = self.bitmap.clone()
			bitmap.bitmap[i] = ord(player)
			future = TTTBoardState(bitmap, self, self.turn + 1, player)

			futures.append(future)

		return futures


	# V3: внешняя оценочная функция на C
	def estimate_utility_v3(self):
		utility_x = bytes(4) # Память для возвратных значений
		utility_o = bytes(4) # не надо так делать - bytes вообще-то read-only
		winner = bytes(1)

		lib.estimate_utility_v2c(
			bytes(self.bitmap.bitmap),
			self.bitmap.w,
			self.bitmap.h,
			5,
			utility_x,
			utility_o,
			winner
		)

		self.utility_x = int.from_bytes(utility_x, "little")
		self.utility_o = int.from_bytes(utility_o, "little")
		self.utility = self.utility_x - self.utility_o
		self.base_utility = self.utility
		self.winner = winner[0]
