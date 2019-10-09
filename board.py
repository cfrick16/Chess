from graphics import *

def midpoint(p1, p2):
	return Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)

def midpoint_rect(rect):
	return midpoint(rect.p1, rect.p2)

class Board:

	def __init__(self, size, window):
		self.size = size
		self.selected = None
		self.window = window
		self.squares = list()
		self.possible_moves = None
		self.white_pieces = []
		self.black_pieces = []

	def preset_pieces(self):
		for i in range(0,8):
			self.white_pieces.append(Piece("pawn", "white", "pieces/WhitePawn.png",self.squares[i][1]))
			self.black_pieces.append(Piece("pawn", "black", "pieces/BlackPawn.png", self.squares[i][6]))
		
		self.white_pieces.append(Piece("rook", "white", "pieces/WhiteRook.png", self.squares[0][0]))
		self.white_pieces.append(Piece("rook", "white", "pieces/WhiteRook.png", self.squares[7][0]))
		self.black_pieces.append(Piece("rook", "black", "pieces/BlackRook.png", self.squares[7][7]))
		self.black_pieces.append(Piece("rook", "black", "pieces/BlackRook.png", self.squares[0][7]))
		
		self.white_pieces.append(Piece("knight", "white", "pieces/WhiteKnight.png", self.squares[1][0]))
		self.white_pieces.append(Piece("knight", "white", "pieces/WhiteKnight.png", self.squares[6][0]))
		self.black_pieces.append(Piece("knight", "black", "pieces/BlackKnight.png", self.squares[1][7]))
		self.black_pieces.append(Piece("knight", "black", "pieces/BlackKnight.png", self.squares[6][7]))

		self.white_pieces.append(Piece("bishop", "white", "pieces/WhiteBishop.png", self.squares[2][0]))
		self.black_pieces.append(Piece("bishop", "black", "pieces/BlackBishop.png", self.squares[2][7]))
		
		self.white_pieces.append(Piece("bishop", "white", "pieces/WhiteBishop.png", self.squares[5][0]))
		self.black_pieces.append(Piece("bishop", "black", "pieces/BlackBishop.png", self.squares[5][7]))
		
		self.white_pieces.append(Piece("queen", "white", "pieces/WhiteQueen.png", self.squares[4][0]))
		self.black_pieces.append(Piece("queen", "black", "pieces/BlackQueen.png", self.squares[4][7]))

		self.white_pieces.append(Piece("king", "white", "pieces/WhiteKing.png", self.squares[3][0]))
		self.black_pieces.append(Piece("king", "black", "pieces/BlackKing.png", self.squares[3][7]))

	def make_checker_board(self):
		blocksize = self.size/8
		for x in range(0, 8):
			l = list()
			for y in range(0, 8):
				r = Rectangle(Point(x*blocksize,y*blocksize), 
							  Point((x+1)*blocksize,(y+1)*blocksize))
				l.append(Square(x, y, r, self.window))
			self.squares.append(l)
		self.preset_pieces()
		self.updateUI()
		self.resetColors()

	def getSquare(self, p):
		square_size = self.size/8
		return self.squares[int(p.x/square_size)][int(p.y/square_size)]

	def getSquare2(self, t):
		return self.squares[t[0]][t[1]]

	def endgame(self, losing_color):
		end = Entry(Point(self.size/2, self.size/2), 10)
		end.setFill("Yellow")
		end.setSize(35)
		end.setStyle("bold")
		if losing_color == "black":
			end.setText("White Wins")
		else:
			end.setText("Black Wins")
		print("ENDGAME")
		end.draw(self.window)


	# 0: Empty, 1: Friendly, 2: Enemy
	def getStateMap(self, color):
		mat = []
		for row in self.squares:
			l = []
			for square in row:
				if square.isEmpty():
					l.append(0)
				elif square.isFriend(color):
					l.append(1)
				else:
					l.append(2)
			mat.append(l)
		return mat
	
	def resetColors(self):
		for x in range(0, 8):
			for y in range(0, 8):
				r = self.squares[x][y].rect
				if((x + y) % 2 == 1):
					r.setFill("grey")
					r.setOutline("grey")
				else:
					r.setFill("white")
					r.setOutline("white")
				
	def handleClick(self, point, color):
		self.resetColors()
		square = self.getSquare(point)

		if self.possible_moves is not None and (square.x,square.y) in self.possible_moves:
			return self.move(square)
		elif square.piece is None or square.piece.color is not color:
			return None
		else:
			self.select(square)
			return None

	def select(self, square):
		self.selected = square.piece
		self.possible_moves = list(self.selected.get_possible_moves(
			self.getStateMap(self.selected.color)))
		for m in self.possible_moves:
			self.squares[m[0]][m[1]].mark()

	def move(self, square):
		ret = self.selected.move(square)
		self.selected = None
		self.possible_moves = None
		return ret



	def updateUI(self):
		for w in self.white_pieces:
			w.updateUI(self.window)
		for b in self.black_pieces:
			b.updateUI(self.window)

	def get_all_possible_moves(self, color):
		ret = []
		if color == "white":
			for w in self.white_pieces:
				x = list(w.get_possible_moves(self.getStateMap("white")))
				if len(x) > 0:
					ret.append((w,x))

		else:
			for b in self.black_pieces:
				x = list(b.get_possible_moves(self.getStateMap("black")))
				if len(x) > 0:
					ret.append((b,x))
		return ret

class Square:

	def __init__(self, x, y, rect, window, piece=None):
		self.rect = rect
		self.piece = None
		self.x = x
		self.y = y
		self.rect.draw(window)
		self.piece = piece

	def isEmpty(self):
		return self.piece == None

	def isEnemy(self, color):
		return not self.isEmpty() and self.piece.color != color

	def isFriend(self, color):
		return not self.isEmpty() and self.piece.color == color

	def setPiece(self,piece):
		self.piece = piece

	def removePiece(self):
		p = self.piece
		self.piece = None
		return p

	def mark(self):
		if(self.piece == None):
			self.rect.setFill("blue")
		else:
			self.rect.setFill("red")

	def fill(self, color):
		self.rect.setFill(color)

	def reset_fill(self):
		if (self.x + self.y) % 2 == 0:
			self.rect.setFill("white")
		else:
			self.rect.setFill("grey")

class Piece:

	def __init__(self, t, color, img, square):
		self.type = t
		self.color = color
		self.removeImage = None
		self.pic = img
		self.image = Image(midpoint_rect(square.rect), img)
		self.first_move = True
		self.square = square
		self.square.setPiece(self)
		if t == "pawn":
			self.value = 1
		elif t == "bishop":
			self.value = 3
		elif t == "knight":
			self.value = 3
		elif t == "rook":
			self.value = 5
		elif t == "queen":
			self.value = 10
		elif t == "king":
			self.value = 100000
		

	def updateUI(self, window):
		if self.removeImage is not None:
			self.removeImage.undraw()
			self.removeImage = None
		if self.image is not None and not self.image.canvas:
			self.image.draw(window)

	def move(self, square):
		ret = 0
		self.removeImage = self.image
		self.square.removePiece()
		self.square = square
		if self.square.isEnemy(self.color):
			ret = self.square.piece.destroy()
		self.square.setPiece(self)
		self.image = Image(midpoint_rect(self.square.rect), self.pic)
		self.first_move = False
		if self.type == "pawn" and (self.square.y == 0 or self.square.y == 7):
			self.pawn_convert()

		return ret

	def pawn_convert(self):
		self.type = "queen"
		if self.color == "white":
			self.pic = "pieces/WhiteQueen.png"
		else:
			self.pic = "pieces/BlackQueen.png"
		self.image = Image(midpoint_rect(self.square.rect), self.pic)
		self.value = 10

	def mock_move(self, square):
		if self.value == 0:
			return None, None, None, None
		ret = 0
		start_square = self.square
		self.square = square
		destroyed_piece = self.square.removePiece()
		if destroyed_piece is not None:
			ret = destroyed_piece.value
			destroyed_piece.value = 0
		self.square.setPiece(self)
		f = self.first_move
		self.first_move = False
		start_square.setPiece(None)
		return ret, start_square, f, destroyed_piece

	def undo_mock_move(self, old_value, start_square, first_move, destroyed_piece):
		end_square = self.square
		self.square = start_square
		start_square.setPiece(self)
		self.first_move = first_move
		end_square.setPiece(destroyed_piece)
		if destroyed_piece is not None:
			destroyed_piece.value = old_value

	def destroy(self):
		self.removeImage = self.image
		self.image = None
		v = self.value
		self.value = 0
		return v

	def coordinates(self):
		return (self.square.x, self.square.y)

	def get_possible_moves(self, stateMap):
		if self.value == 0:
			return 
		cordinates = []
		start_x, start_y = self.square.x, self.square.y
		if(self.type == "rook"):
			for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
				x, y = start_x + direction[0], start_y + direction[1]
				while(x in range(0,8) and y in range(0, 8) and stateMap[x][y] != 1 ):
					yield (x,y)
					if stateMap[x][y] == 2:
						break
					x += direction[0]
					y += direction[1]



		elif(self.type == "bishop"):
			for direction in [(1,1), (1,-1), (-1,1), (-1,-1)]:
				x, y = start_x + direction[0], start_y + direction[1]
				while(x in range(0,8) and y in range(0, 8) and stateMap[x][y] != 1 ):
					yield (x,y)
					if stateMap[x][y] == 2:
						break
					x += direction[0]
					y += direction[1]


		elif(self.type == "knight"):
			for direction in [(2,1), (2,-1), (-2,1), (-2, -1), (1,2), (1, -2), (-1,2), (-1,-2)]:
				x, y = start_x + direction[0], start_y + direction[1]
				if(x in range(0,8) and y in range(0, 8) and stateMap[x][y] != 1 ):
					yield (x,y)

		
		elif(self.type == "king"):
			for direction in [(0,1), (0,-1), (1,0), (-1,0),(1,1), (1,-1), (-1,1), (-1,-1)]:
				x, y = start_x + direction[0], start_y + direction[1]
				if(x in range(0,8) and y in range(0, 8) and stateMap[x][y] != 1 ):
					yield (x,y)

		
		elif(self.type == "queen"):
			for direction in [(0,1), (0,-1), (1,0), (-1,0),(1,1), (1,-1), (-1,1), (-1,-1)]:
				x, y = start_x + direction[0], start_y + direction[1]
				while(x in range(0,8) and y in range(0, 8) and stateMap[x][y] != 1 ):
					yield (x,y)
					if stateMap[x][y] == 2:
						break
					x += direction[0]
					y += direction[1]

		elif(self.type == "pawn"):
			f = 1
			x = start_x
			y = start_y
			bound = y < 7
			if self.color == "black":
				bound = y > 0
				f = -1

			if bound and x < 7 and stateMap[x+1][y+f] == 2:
				yield (x + 1, y + f)
			if bound and x > 0 and stateMap[x-1][y+f] == 2:
				yield (x - 1, y + f)
			if bound and stateMap[x][y+f] == 0:
				yield (x, y + f)
			if self.first_move and stateMap[x][y+f] == 0 and stateMap[x][y+2*f] == 0:
				yield (x, y + 2*f)

