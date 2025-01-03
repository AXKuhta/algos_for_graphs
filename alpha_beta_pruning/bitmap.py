
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
			yield bitmap[w-1+w*i::w-1][:w-i]

		for i in range(1, w):
			yield bitmap[w-1-i::w-1][:w-i]

	def __str__(self):
		return "\n".join([x.decode() for x in self.rows()])

def test():
	hor = 	b"......."\
		b"......."\
		b"......."\
		b"......."\
		b"......."\
		b"xxxx..."

	vert = 	b"......."\
		b"......."\
		b"..x...."\
		b"..x...."\
		b"..x...."\
		b"..x...."

	diag =	b"...o..."\
		b"....o.."\
		b"x....o."\
		b".x....o"\
		b"..x...."\
		b"...x..."\

	diag2 =	b"......o"\
		b"...y.ox"\
		b"..y.ox."\
		b".y.ox.."\
		b"y..x..."\
		b"......."\

	print("=== Rows ===")
	for row in Bitmap(hor, 7, 6).rows():
		print(row)

	print("=== Cols ===")
	for col in Bitmap(vert, 7, 6).cols():
		print(col)

	print("=== Diag ===")
	for trace in Bitmap(diag, 7, 6).pri_diag():
		print(trace)

	print("=== Diag2 ===")
	for trace in Bitmap(diag2, 7, 6).sec_diag():
		print(trace)

