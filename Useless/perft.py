from board import *
from numpy import array
import time
import os


test_board = Board()

bitboards = test_board.bitboards
data = test_board.board_data



def perft(depth, nodes, board):
    if depth == 0:
        nodes += 1

    else:
        moves = board.return_moves()
        for move in moves:
            copy_board = Board(*board.copy_position())

            if copy_board.make_move(move) == False:
                continue
            else:
                perft(depth - 1, nodes, copy_board)


nodes = array(0)
uintt = test_board.bitboards[0]
depth = int(input("Depth = "))
stime = time.time()
perft(depth, nodes, test_board)
os.system('cls')
print("Nodes =", nodes)
print("Time =", time.time() - stime)