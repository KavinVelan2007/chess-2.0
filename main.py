from numpy import uint64 as uint

WHITE_PAWNS = uint(71776119061217280)
WHITE_KING = uint(576460752303423488)
WHITE_QUEEN = uint(1152921504606846976)

BLACK_PAWNS = uint(65280)
BLACK_KING = uint(8)
BLACK_QUEEN = uint(16)

def disp(n):
    for _ in range(8):
        for _ in range(8):
            print('*' if n & uint(1) else '-',end=' ')
            n = n >> uint(1)
        print()

disp(BLACK_PAWNS | WHITE_PAWNS | BLACK_KING | BLACK_QUEEN | WHITE_KING | WHITE_QUEEN)