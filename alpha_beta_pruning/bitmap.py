
class Bitmap:
	def __init__(self, bitmap, w, h):
		self.bitmap = bytearray(bitmap)
		self.w = w
		self.h = h

	def clone(self):
		return Bitmap(b"" + self.bitmap, self.w, self.h)

	def rows(self):
		bitmap = self.bitmap
		w = self.w
		h = self.h

		for i in range(h):
			yield bitmap[i*w:i*w+w]

	def cols(self):
		bitmap = self.bitmap
		w = self.w
		h = self.h

		for i in range(w):
			yield bitmap[i::w]

	def pri_diag(self):
		bitmap = self.bitmap
		w = self.w
		h = self.h

		for i in range(h):
			yield bitmap[w*i::w+1]

		for i in range(1, w):
			yield bitmap[i::w+1][:w-i]

	def sec_diag(self):
		bitmap = self.bitmap
		w = self.w
		h = self.h

		for i in range(h):
			yield bitmap[w-1+w*i::w-1]

		for i in range(1, w):
			yield bitmap[w-1-i::w-1][:w-i]

	def __str__(self):
		return "=== bitmap ===\n" + "\n".join([x.decode() for x in self.rows()])
