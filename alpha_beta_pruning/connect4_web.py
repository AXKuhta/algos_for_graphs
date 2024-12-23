from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus
from urllib.parse import parse_qs
import webbrowser

from bitmap import Bitmap
from connect4_core import BoardState

class Connect4Handler(BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def do_GET(self):
		if self.path == "/":
			self.handle_index()
		else:
			self.text_response(f"Unknown path [{self.path}]", status=HTTPStatus.NOT_FOUND)

	def board_as_table(self, board, moves=""):
		rows = []

		for i in range(board.bitmap.h):
			cols = []

			for j in range(board.bitmap.w):
				c = chr(board.bitmap.bitmap[i*board.bitmap.w + j])

				if c == "x":
					cols.append("<td class='red'></td>")
				elif c == "o":
					cols.append("<td class='yellow'></td>")
				elif c == "." and moves:
					turn = board.turn + 1
					moved = "x" if board.moved == "o" else "o"
					bmcopy = bytearray(board.bitmap.bitmap)

					# Отметить ход
					bmcopy[i*board.bitmap.w + j] = ord(moved)

					# Окрыть позицию выше, если возможно
					if i > 0:
						bmcopy[i*board.bitmap.w - board.bitmap.w + j] = ord(".")

					bmcopy = bmcopy.decode()

					cols.append("<td class=''>")
					cols.append("<form action='/' method='POST'>")
					cols.append(f"<input type='hidden' name='state' value='{bmcopy}'>")
					cols.append(f"<input type='hidden' name='moved' value='{moved}'>")
					cols.append(f"<input type='hidden' name='turn' value='{turn}'>")
					cols.append("<button>")
					cols.append("</button>")
					cols.append("</form>")
					cols.append("</td>")
				else:
					cols.append("<td class=''></td>")

			rows.append("<tr>")
			rows.append( "".join(cols) )
			rows.append("</tr>")

		return "<table>" + "".join(rows) + "</table>"


	def do_POST(self):
		length = self.headers.get('content-length')
		payload = self.rfile.read( int(length) )
		params = parse_qs(payload)

		state = params.get(b"state")[0]
		turn = int(params.get(b"turn")[0])
		moved = params.get(b"moved", [b""])[0].decode()

		loc_bm = Bitmap(state, 7, 6)
		loc = BoardState(loc_bm, None, turn, moved)

		if loc.moved:
			loc.explore()

		opener = 	"<!DOCTYPE html>"\
				"<style>"\
				"body { font-family: system-ui; font-size: 20px; }"\
				"td { width: 1rem; height: 1rem; text-align: center; border: 1px solid black; }"\
				"td form { height: inherit; }"\
				"td form button { display: block; height: 100%; width: 100%; border: none; }"\
				".red { background-color: red; }"\
				".yellow { background-color: yellow; }"\
				".option { display: inline-block; padding: 1rem; margin: 1rem; border: 1px solid black; }"\
				"</style>"

		doc = [opener]

		def recurse_options(loc):
			options = []

			for i, s in enumerate(loc.future):
				option = 	"<div class='option'>"\
						f"{self.board_as_table(s)}"\
						f"Hoisted: {s.utility}<br>"\
						f"Utility: {s.base_utility}"\
						"<details>"\
						f"<summary>Futures: {len(s.future)}</summary>"\
						f"{recurse_options(s)}"\
						"</details>"\
						"</div>"

				options.append(option)

			return "".join(options)


		moves = ""

		if loc.moved:
			# Компьютер
			if loc.future:
				#doc.append("<div>Computer has options:</div>")
				#doc.append(recurse_options(loc))

				if loc.moved == "o":
					loc = max(loc.future, key=lambda x: x.utility)
				else:
					loc = min(loc.future, key=lambda x: x.utility)


				if not loc.future:
					if loc.winner:
						doc.append("<div>The computer won</div>")
					else:
						doc.append("<div>No winners</div>")
				else:
					doc.append("<div>Computer makes a move:</div>")
					moves = "x"
			else:
				moves = ""
				if loc.winner:
					doc.append("<div>You won</div>")
				else:
					doc.append("<div>No winners</div>")
		else:
			moves="x"

		present = 	"<div class='option'>"\
				f"{self.board_as_table(loc, moves=moves)}"\
				"</div>"

		doc.append(present)

		if moves:
			doc.append("<div>Make your move</div>")

		self.text_response("".join(doc))

	def handle_index(self):
		init_state = 	"       "\
				"       "\
				"       "\
				"       "\
				"       "\
				"......."\

		response = 	"<!DOCTYPE html>"\
				"<div>Welcome to connect4</div>"\
				"<form action='/' method='POST'>"\
				f"<input type='hidden' name='state' value='{init_state}'>"\
				f"<input type='hidden' name='moved' value=''>"\
				f"<input type='hidden' name='turn' value='0'>"\
				"<input type='submit' value='Play'>"\
				"</form>"

		self.text_response(response)

	def text_response(self, text, status=HTTPStatus.OK):
		payload = text.encode()
		self.send_response(status)
		self.send_header("Content-Length", len(payload))
		self.end_headers()
		self.wfile.write(payload)

def run(server_class=HTTPServer, handler_class=Connect4Handler):
	server_address = ('', 8000)
	httpd = server_class(server_address, handler_class)
	webbrowser.open("http://localhost:8000")
	httpd.serve_forever()

run()
