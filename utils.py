from numpy import uint64 as uint

def count_bits(bit_board):
    c = 0
    while bit_board:
        bit_board &= bit_board - uint(1)
        c += 1
    return c

'''
def least_significant_bit_count(bit_board):
    return int(bit_board) & -int(bit_board)
'''

def most_significant_bit_count(bitboard):
    ndx = 0
    n = bitboard // 2
    while n:
        n //= 2
        ndx += 1
    return ndx

def chess_square_to_index(position: str):
    return (ord(position[0]) - ord('A')) + ((8 - int(position[1])) * 8)