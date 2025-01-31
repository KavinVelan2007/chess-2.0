from numpy import uint64 as uint,uint32

with open('chess-2.0/fenString.txt','r') as file:
	fenString = file.read().replace('\n', '')
	file.close()

def count_bits(bit_board):
	c = 0
	while bit_board:
		bit_board &= bit_board - uint(1)
		c += 1
	return c


def least_significant_bit_count(bit_board):
	return count_bits(bit_board - uint(1)) - count_bits(bit_board) + 1


def translate_from_fen(fen: str):
	board = [[' ' for _ in range(8)] for _ in range(8)]
	fen = fen.split(' ')
	position = fen[0].split('/')
	for rank in range(len(position)):
		file = 0
		index = 0
		while index < len(position[rank]):
			if position[rank][index].isalpha():
				board[rank][file] = position[rank][index]
				file += 1
			elif '1' <= position[rank][index] <= '9':
				file += int(position[rank][index])
			index += 1
	data = uint32(0)
	if fen[1] == 'b':
		data |= uint32(1)
	if fen[2] != '-':
		bit_positions_for_castling = {
			'K': 1,
			'Q': 2,
			'k': 3,
			'q': 4
		}
		for side in fen[2]:
			data |= (uint32(1) << uint32(bit_positions_for_castling[side]))
	if fen[3] != '-':
		data |= uint32(1 << 5)
		pos = fen[3]
		index = uint32(ord(pos[0]) - ord('a') + (8 - int(pos[1])) * 8)
		data |= index << uint32(6)
	halfMoves = uint32(fen[4])
	data |= ((halfMoves & uint32((1 << 6) - 1)) << uint32(12))
	moves = uint32(fen[5])
	data |= ((moves & uint32((1 << 8) - 1)) << uint(18))
	return board,data

def generate_bitboards_from_board(fen):
	board,data = translate_from_fen(fen)
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
	return (P,N,B,R,Q,K,p,n,b,r,q,k),data

def convert_bitboards_to_2d(bitboards):

	chars = {
		0: 'P',
		1: 'N',
		2: 'B',
		3: 'R',
		4: 'Q',
		5: 'K',
		6: 'p',
		7: 'n',
		8: 'b',
		9: 'r',
		10: 'q',
		11: 'k'
	}

	board = [['' for _ in range(8)] for _ in range(8)]

	for row in range(7,-1,-1):
		for col in range(7,-1,-1):
			pos = row * 8 + col
			for i in range(12):
				if bitboards[i] & (uint(1) << pos):
					board[row][col] = chars[i]
					break
	
	return board[::-1]

def convert_bitboards_to_fen(bitboard,board_data):
	board = convert_bitboards_to_2d(bitboard)
	fen = ''
	for rank in board:
		count = 0
		for square in rank[::-1]:
			if square:
				if count:
					fen += str(count)
					count = 0
				fen += square
			else:
				count += 1
		if count:
			fen += str(count)
		fen += '/'
	fen = fen[:-1][::-1] + ' '
	fen += 'b' if board_data & uint(1) else 'w'
	fen += ' '
	bit_positions_for_castling = {
		1: 'K',
		2: 'Q',
		3: 'k',
		4: 'q'
	}
	castlingPresent = False
	for shift in range(1,5):
		if board_data & (uint(1) << shift):
			fen += bit_positions_for_castling[shift]
			castlingPresent = True
	fen += ' ' if castlingPresent else '- '
	if board_data & (uint(1) << 5):
		pos = (data >> 6) & ((uint(1) << 6) - 1)
		row = 8 - pos // 8 - 1
		col = pos % 8
		fen += f'{chr(97 + col)}{row + 1} '
	else:
		fen += '- '
	halfMoves = board_data >> 12 & uint((1 << 6) - 1)
	fen += str(halfMoves) + ' '
	moves = board_data >> 18 & uint((1 << 8) - 1)
	fen += str(moves)
	return fen

if __name__ == '__main__':
	bitboards,data = generate_bitboards_from_board(fenString)
	print(fenString)
	print(convert_bitboards_to_fen(bitboards,data))