from brains import *
import time


def run(n):
	board = Board()
	stime = time.time()
	for i in range(n):
		board.return_moves()
	print("Done")
	print(f"Time: {time.time() - stime}")
run(5_000_000)