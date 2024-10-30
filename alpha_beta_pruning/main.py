
w = 7
h = 6

def rows(bitmap):
	for i in range(h):
		yield bitmap[i*w:i*w+w]

def cols(bitmap):
	for i in range(w):
		yield bitmap[i::w]

def pri_diag(bitmap):
	for i in range(h):
		yield bitmap[w*i::w+1]

	for i in range(1, w):
		yield bitmap[i::w+1][:w-i]

def sec_diag(bitmap):
	for i in range(h):
		yield bitmap[w-1+w*i::w-1]

	for i in range(1, w):
		yield bitmap[w-1-i::w-1][:w-i]

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
for row in rows(hor):
	print(row)

print("=== Cols ===")
for col in cols(vert):
	print(col)

print("=== Diag ===")
for trace in pri_diag(diag):
	print(trace)

print("=== Diag2 ===")
for trace in sec_diag(diag2):
	print(trace)
