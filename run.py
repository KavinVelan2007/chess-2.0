from brains import *
import time
from fen import *

temp_BITBOARDS, temp_data = generate_bitboards_from_board(fenString)


def run(n):
	board = Board(temp_BITBOARDS, temp_data)
	stime = time.time()
	for i in range(n):
		board.return_moves()
	print("Done")
	print(f"Time: {time.time() - stime}")
	board.print_chess_board()
	board2 = Board(*board.copy())
	board.make_move(board.return_moves().return_move_list()[0])
	board.print_chess_board()
	board2.print_chess_board()
	

run(2_000_000)