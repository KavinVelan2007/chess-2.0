from numpy import uint64 as uint
from data import * 

WHITE_PAWNS = uint(71776119061217280)
WHITE_KING = uint(576460752303423488)
WHITE_QUEEN = uint(1152921504606846976)
WHITE_ROOKS = uint(9295429630892703744)
WHITE_KNIGHTS = uint(4755801206503243776)
WHITE_BISHOPS = uint(2594073385365405696)


BLACK_PAWNS = uint(65280)
BLACK_KING = uint(8)
BLACK_QUEEN = uint(16)
BLACK_ROOKS = uint(129)
BLACK_KNIGHTS = uint(66)
BLACK_BISHOPS = uint(36)


def print_bitboard(bit_board):
    c = uint(0)
    print('    A   B   C   D   E   F   G   H')
    print()
    for i in range(8):
        print(i + 1, '  ', end ='')
        for j in range(8):
            print('*   ' if bit_board & (uint(1) << c) else '.   ', end = '')
            c += uint(1)
        print('\n')
    print()
    print('BitBoard Value:', bit_board)


def generate_king_attacks():
    for i in range(64):
        c = uint(0)
        if i % 8 != 0:
            c |= uint(1) << uint(i - 1)
            if i >= 8:
                c |= uint(1) << uint(i - 9)
            if i <= 55:
                c |= uint(1) << uint(i + 7)
        if i % 8 != 7:
            c |= uint(1) << uint(i + 1)
            if i >= 8:
                c |= uint(1) << uint(i - 7)
            if i <= 55:
                c |= uint(1) << uint(i + 9)
        if i >= 8:
            c |= uint(1) << uint(i - 8)
        if i <= 55:
            c |= uint(1) << uint(i + 8)
        print('uint(', c, '),', sep = '')
        

def generate_knight_attacks():
    for i in range(64):
        c = uint(0)
        if i % 8 >= 1:
            if i >= 16:
                c |= uint(1) << uint(i - 17)
            if i <= 47:
                c |= uint(1) << uint(i + 15)
            if i % 8 >= 2:
                if i >= 8:
                    c |= uint(1) << uint(i - 10)
                if i <= 55:
                    c |= uint(1) << uint(i + 6)
        if i % 8 <= 6:
            if i >= 16:
                c |= uint(1) << uint(i - 15)
            if i <= 47:
                c |= uint(1) << uint(i  + 17)
            if i % 8 <= 5:
                if i >= 8:
                    c |= uint(1) << uint(i - 6)
                if i <= 55:
                    c |= uint(1) << uint(i + 10)
        print('uint(', c, '),', sep = '')
        

def generate_rook_occupancy():
    for i in range(64):
        c = uint(0)
        for j in [1,2,3,4,5,6]:
            if i % 8 != j:
                c |= uint(1) << uint(i - i % 8 + j)
            if i // 8 != j:
                c |= uint(1) << uint(j * 8 + i % 8)
        print('uint(', c, '),', sep = '')