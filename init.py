from graphics import *
from board import *
from players import *

size = 600
win = GraphWin(width=size,height=size)



def play(b):

	player1 = None
	player2 = None
	game = int(input("Type 1 for player vs player, 2 for player vs AI, 3 for AI vs AI: "))
	if game == 3:
		level = int(input("What level should the AIs be on (1-5):"))
		player1 = AI(b, "white", level)
		player2 = AI(b, "black", level)
	elif game == 1:
		player1 = Human(b,"white")
		player2 = Human(b,"black")
	elif game == 2:
		level = int(input("What level should the AIs be on (1-5):"))
		player1 = Human(b,"white")
		player2 = AI(b,"black", level)
	else:
		assert(0)

	value_lost = 0
	endgame = False
	while not endgame:
		endgame = player1.removeValue(value_lost)
		value_lost = player1.move()
		endgame = player2.removeValue(value_lost)
		if not endgame:
			value_lost = player2.move()


	

if __name__ == '__main__':
	b = Board(size, win)
	b.make_checker_board()
	play(b)
	win.getMouse()
	win.close()
