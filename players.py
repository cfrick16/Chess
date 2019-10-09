from graphics import *
from board import *
import random
import time

def tiebreak(moves, board):
	best_value = -1000
	best_move = None
	print("Tiebreaker on ", len(moves), " Moves")
	l = []
	for piece, end_location in moves:
		value = 0
		start = piece.coordinates()
		# Dont want to move king
		value -= 20 if piece.type == "king" else 0
		
		# Want to move to center
		value += abs(start[0] - 3.5) - abs(end_location[0] - 3.5)
		value += abs(start[1] - 3.5) - abs(end_location[1] - 3.5)
		
		# Want to open up further options
		old_possibilities = sum(1 for _ in piece.get_possible_moves(board.getStateMap(piece.color)))
		dv, ss, fm, dp = piece.mock_move(board.getSquare2(end_location))
		new_possibilities = sum(1 for _ in piece.get_possible_moves(board.getStateMap(piece.color)))
		piece.undo_mock_move(dv, ss, fm, dp)
		value += (new_possibilities - old_possibilities)

		# Want to move forward
		forward = (-1 if piece.color =="black" else 1) * (end_location[1] - start[1])
		value += forward

		# Move a piece that hasn't been moved before
		if piece.type != "queen":
			value += piece.value + 2 if piece.first_move and forward > 0 else 0

		# if value > best_value:
		# 	best_value = value
		# 	best_move = (piece, end_location)
		for i in range(0, int(value)):
			l.append((piece, end_location))


	if len(l) == 0:
		return moves[random.randint(0,len(moves) - 1)]

	return l[random.randint(0, len(l)-1)]
def getBestMove(board, turn_color, depth_to_go):
	bestValue = -10000000000
	best_moves = None
	possible_moves = board.get_all_possible_moves(turn_color)
	for piece, end_locations in possible_moves:
		for end_location in end_locations:
			# print("Considering ", (piece.square.x, piece.square.y), " to ", end_location)
			delta_value, start_square, first_move, destroyed_piece  = piece.mock_move(board.getSquare2(end_location))
			old_value = delta_value
			if delta_value < 100:
				delta_value -= getBestValue(board, "white" if turn_color == "black" else "black", depth_to_go-1,"\t")
			piece.undo_mock_move(old_value,start_square, first_move, destroyed_piece)
			if bestValue < delta_value:
				bestValue = delta_value
				best_moves = [(piece, end_location)]
			elif bestValue == delta_value:
				best_moves.append((piece,end_location))
	print("best_value: ", bestValue)
	if depth_to_go == 1:
		bestValue -= 1
	return tiebreak(best_moves, board), bestValue


def getBestValue(board, turn_color, depth_to_go, tabs):
	if depth_to_go == 0:
		return 0
	bestValue = -10000000000
	possible_moves = board.get_all_possible_moves(turn_color)
	# print("Looking at all ", turn_color, " options at depth ", depth_to_go)
	for piece, end_locations in possible_moves:
		for end_location in end_locations:
			start = piece.coordinates()
			assert(piece.color == turn_color)
			delta_value, start_square, first_move, destroyed_piece  = piece.mock_move(board.getSquare2(end_location))
			if delta_value is not None:
				old_value = delta_value
				if delta_value < 100:
					delta_value -= getBestValue(board, "white" if turn_color == "black" else "black", depth_to_go-1, tabs + "\t")
				piece.undo_mock_move(old_value,start_square, first_move, destroyed_piece)
				bestValue = max (bestValue, delta_value)
	return bestValue

class Player:

	def __init__(self, board, color):
		self.board = board
		self.value = 100040 
		self.color = color
		# self.value = sum(p.value for p in pieces)

	def removeValue(self, x):
		self.value -= x
		if self.value < 100000:
			self.board.endgame(self.color)
			return True
		return False

	def move(self):
		assert(0)

class AI(Player):

	def __init__(self, board, color, level):
		self.level = level
		Player.__init__(self, board, color)

	def move(self):
		move, value = getBestMove(self.board, self.color, self.level)
		# print("Chose ", (move[0].square.x, move[0].square.y), " to ", move[1], 
			# " for a value of ", value)
		return self.make_move(move[0], self.board.getSquare2(move[1]))

	def make_move(self, piece, end_location):

		piece.square.fill("gold")
		end_location.fill("gold")
		time.sleep(.8)
		piece.square.reset_fill()
		end_location.reset_fill()
		points_taken = piece.move(end_location)
		self.board.updateUI()
		return points_taken

class Human(Player):

	def __init__(self, board, color):
		Player.__init__(self,board, color)

	def move(self):
		points_taken = None
		while points_taken is None:
			points_taken = self.board.handleClick(
				self.board.window.getMouse(), self.color)
		
		self.board.updateUI()
		return points_taken
