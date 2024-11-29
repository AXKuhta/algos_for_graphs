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

	def board_as_table(self, board):
		rows = []

		for line in str(board).split("\n"):
			cols = []
			for c in line:
				if c == "x":
					classname = "red"
				elif c == "o":
					classname = "yellow"
				else:
					classname = ""
				cols.append(f"<td class='{classname}'>")
				#cols.append(c)
				cols.append("</td>")

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
		loc.explore()

		# Компьютер
		if loc.future:
			status = "Computer makes a move"
			if loc.moved == "o":
				loc = max(loc.future, key=lambda x: x.utility)
			else:
				loc = min(loc.future, key=lambda x: x.utility)

			if not loc.future:
				status = "The computer won"
		else:
			status = "You won!"

		present = 	f"<div>{status}</div>"\
				"<div class='option'>"\
				f"{self.board_as_table(loc.bitmap)}"\
				"</div>" if loc.moved else ""

		options = []

		for i, s in enumerate(loc.future):
			option = 	"<div class='option'>"\
					"<form action='/' method='POST'>"\
					f"{self.board_as_table(s.bitmap)}"\
					f"<input type='hidden' name='state' value='{s.bitmap.bitmap.decode()}'>"\
					f"<input type='hidden' name='moved' value='{s.moved}'>"\
					f"<input type='hidden' name='turn' value='{s.turn}'>"\
					"<input type='submit' value='Select'>"\
					"</form>"\
					"</div>"

			options.append(option)

		if options:
			options = ["<div>Make your move</div>"] + options

		response = 	"<!DOCTYPE html>"\
				"<style>"\
				"body { font-family: system-ui; font-size: 20px; }"\
				"td { width: 1rem; height: 1rem; text-align: center; border: 1px solid black; }"\
				".red { background-color: red; }"\
				".yellow { background-color: yellow; }"\
				".option { display: inline-block; padding: 1rem; margin: 1rem; border: 1px solid black; }"\
				"</style>"\
				f"{present}"\
				"" + "".join(options)

		self.text_response(response)

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
