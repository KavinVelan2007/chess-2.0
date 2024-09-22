from numpy import uint64 as uint

def count_bits(bit_board):
    c = 0
    while bit_board:
        bit_board &= bit_board - uint(1)
        c += 1
    return c


def least_significant_bit_count(bit_board):
    return count_bits(bit_board - uint(1)) - count_bits(bit_board) + 1


def most_significant_bit_count(bitboard):
    ndx = 0
    n = bitboard // 2
    while n:
        n //= 2
        ndx += 1
    return ndx