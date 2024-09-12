from numpy import uint64 as uint

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


def p_bb(bit_board):
    c = uint(0)
    print('    A   B   C   D   E   F   G   H')
    print()
    for i in range(8):
        print(i + 1, '  ', end ='')
        for j in range(8):
            print('*   ' if bit_board & (uint(1) << c) else '.   ', end = '')
            c += uint(1)
        print('\n')