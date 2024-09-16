from numpy import uint64 as uint

with open('fenString.txt','r') as file:
	fenString = file.read()
	file.close()

def translate_from_fen(fen: str):
	board = [[' ' for _ in range(8)] for _ in range(8)]
	fen = fen.split('/')
	for rank in range(len(fen)):
		file = 0
		index = 0
		while index < len(fen[rank]):
			if fen[rank][index].isalpha():
				board[rank][file] = fen[rank][index]
				file += 1
			elif '1' <= fen[rank][index] <= '9':
				file += int(fen[rank][index])
			index += 1
	return board

def generate_bitboards_from_board(fen):
    board = translate_from_fen(fen)
    p = r = b = n = q = k = P = R = B = N = Q = K = uint(0)
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'p':
                p |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'r':
                r |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'b':
                b |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'n':
                n |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'q':
                q |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'k':
                k |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'P':
                P |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'R':
                R |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'B':
                B |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'N':
                N |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'Q':
                Q |= uint(1) << uint(row * 8 + col)
            elif board[row][col] == 'K':
                K |= uint(1) << uint(row * 8 + col)
    return (P,N,B,R,Q,K,p,n,b,r,q,k)
            