from numpy import uint64 as uint

with open('fenString.txt','r') as file:
	fenString = file.read()
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
    print(fen)
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
    data = uint(0)
    if fen[1] == 'b':
        data |= (uint(1) << uint(31))
    if fen[2] != '-':
        bit_positions_for_castling = {
            'K': 30,
            'Q': 29,
            'k': 28,
            'q': 27
        }
        for side in fen[2]:
            data |= (uint(1) << uint(bit_positions_for_castling[side]))
    if fen[3] != '-':
        data |= (uint(1) << uint(26))
        pos = fen[3]
        index = uint(ord(pos[0]) - ord('a') + (8 - int(pos[1])) * 8)
        while index:
            ls1b = least_significant_bit_count(index)
            data |= (uint(1) << uint(ls1b + 20))
            index &= index - uint(1)
    halfMoves = uint(fen[4])
    return board,data,halfMoves

def generate_bitboards_from_board(fen):
    board,data,halfMoves = translate_from_fen(fen)
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
    return (P,N,B,R,Q,K,p,n,b,r,q,k),data,halfMoves