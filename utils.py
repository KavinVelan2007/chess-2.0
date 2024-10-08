from numpy import uint64 as uint, array

def count_bits(bit_board):
    c = 0
    while bit_board:
        bit_board &= bit_board - uint(1)
        c += 1
    return c


def least_significant_bit_count(bit_board):
    return int(bit_board).bit_length() - 1


def most_significant_bit_count(bitboard):
    ndx = 0
    n = bitboard // 2
    while n:
        n //= 2
        ndx += 1
    return ndx

def chess_square_to_index(position: str):
    return (ord(position[0]) - ord('A')) + ((8 - int(position[1])) * 8)

'''
ls1b_indices = array([
    0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63
])

def least_significant_bit_count(bb):
    debruijn64 = uint(0x03f79d71b4cb0a89)
    return ls1b_indices[int(((bb ^ (bb-uint(1))) * debruijn64) >> uint(58))]
'''