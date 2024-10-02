from numpy import uint64 as uint, uint32, array, zeros, trim_zeros
import time
import sys
import random
from utils import *
random.seed(time.time())
from data import *


def print_bitboard(bit_board):
    c = uint(0)
    for i in range(8):
        print(8 - i, "    ", end="")
        for j in range(8):
            print("1   " if bit_board & (uint(1) << c) else ".   ", end="")
            c += uint(1)
        print("\n")
    print()
    print("      A   B   C   D   E   F   G   H")
    print()
    print("BitBoard Value:", bit_board)
    print("\n")


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
        print("uint(", c, "),", sep="")


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
                c |= uint(1) << uint(i + 17)
            if i % 8 <= 5:
                if i >= 8:
                    c |= uint(1) << uint(i - 6)
                if i <= 55:
                    c |= uint(1) << uint(i + 10)
        print("uint(", c, "),", sep="")


def generate_rook_occupancy():
    for i in range(64):
        c = uint(0)
        for j in [1, 2, 3, 4, 5, 6]:
            if i % 8 != j:
                c |= uint(1) << uint(i - i % 8 + j)
            if i // 8 != j:
                c |= uint(1) << uint(j * 8 + i % 8)
        print("uint(", c, "),", sep="")


def generate_bishop_occupancy():
    for i in range(64):
        n = uint(0)
        r, c = i // 8, i % 8
        row, col = r + 1, c + 1
        while row <= 6 and col <= 6:
            n |= uint(1) << uint(row * 8 + col)
            row += 1
            col += 1
        row, col = r - 1, c + 1
        while row >= 1 and col <= 6:
            n |= uint(1) << uint(row * 8 + col)
            row -= 1
            col += 1
        row, col = r + 1, c - 1
        while row <= 6 and col >= 1:
            n |= uint(1) << uint(row * 8 + col)
            row += 1
            col -= 1
        row, col = r - 1, c - 1
        while row >= 1 and col >= 1:
            n |= uint(1) << uint(row * 8 + col)
            row -= 1
            col -= 1
        print(f"uint({n})", end=",")


def fill_occupancy(value, bit_board):
    occupancy = uint(0)
    c = uint(0)
    while bit_board:
        if value & (uint(1) << c):
            occupancy |= uint(1) << uint(
                count_bits(bit_board - uint(1)) - count_bits(bit_board) + uint(1)
            )
        bit_board &= bit_board - uint(1)
        c += uint(1)
    return occupancy


seed = uint32(time.time())


def random_number_generate():
    def rand():
        global seed
        seed ^= seed << uint32(13)
        seed ^= seed >> uint32(17)
        seed ^= seed << uint32(5)
        return seed

    return (
        (uint(rand() & uint32(0xFFFF)))
        | (uint(rand() & uint32(0xFFFF)) << uint(16))
        | (uint(rand() & uint32(0xFFFF)) << uint(32))
        | (uint(rand() & uint32(0xFFFF)) << uint(48))
    )


def generate_bishop_attacks(i, mask):
    n = uint(0)
    r, c = i // 8, i % 8
    row, col = r + 1, c + 1
    while row <= 7 and col <= 7:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row += 1
        col += 1
    row, col = r - 1, c + 1
    while row >= 0 and col <= 7:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row -= 1
        col += 1
    row, col = r + 1, c - 1
    while row <= 7 and col >= 0:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row += 1
        col -= 1
    row, col = r - 1, c - 1
    while row >= 0 and col >= 0:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row -= 1
        col -= 1
    return n


def generate_rook_attacks(i, mask):
    row = i // 8
    col = i % 8
    n = uint(0)
    for r in range(row + 1, 8):
        n |= uint(1) << uint(r * 8 + col)
        if mask & (uint(1) << uint(r * 8 + col)):
            break
    for r in range(row - 1, -1, -1):
        n |= uint(1) << uint(r * 8 + col)
        if mask & (uint(1) << uint(r * 8 + col)):
            break
    for c in range(col + 1, 8):
        n |= uint(1) << uint(row * 8 + c)
        if mask & (uint(1) << uint(row * 8 + c)):
            break
    for c in range(col - 1, -1, -1):
        n |= uint(1) << uint(row * 8 + c)
        if mask & (uint(1) << uint(row * 8 + c)):
            break
    return n


def generate_magic_numbers(
    position, bits_present, piece
):  # For the piece parameter, bishop = 0, rook = 1
    occupancy = []
    attack = []
    used_attacks = []
    current_occupancy = (
        ROOK_OCCUPANCY[position] if piece else BISHOP_OCCUPANCY[position]
    )
    for i in range(uint(1) << uint(bits_present)):
        occupancy += [fill_occupancy(uint(i), current_occupancy)]
        attack += [
            generate_rook_attacks(position, occupancy[i])
            if piece
            else generate_bishop_attacks(position, occupancy[i])
        ]

    for i in range(100000000):
        magic_number = uint(random.randint(0, (1 << 64) - 1)) & uint(
            random.randint(0, (1 << 64) - 1)
        )
        if (
            count_bits((current_occupancy * magic_number) & uint(0xFF00000000000000))
            < 6
        ):
            continue
        used_attacks = [uint(0) for i in range(uint(1) << uint(bits_present))]

        index = 0
        failed = False

        while not failed and index < (uint(1) << uint(bits_present)):
            magic_index = (occupancy[index] * magic_number) >> uint(64 - bits_present)
            if used_attacks[magic_index] == uint(0):
                used_attacks[magic_index] = attack[index]
            elif used_attacks[magic_index] != attack[index]:
                failed = True
            index += 1
        if not failed:
            return magic_number
    return uint(0)


def init_magic_tables():
    global ROOK_ATTACKS, BISHOP_ATTACKS
    ROOK_ATTACKS = array([[uint(0) for x in range(1 << 12)] for i in range(64)])
    BISHOP_ATTACKS = array([[uint(0) for x in range(1 << 9)] for i in range(64)])
    for i in range(64):
        for j in range(1 << ROOK_OCCUPANCY_BITS[i]):
            magic_index = (
                fill_occupancy(uint(j), ROOK_OCCUPANCY[i]) * ROOK_MAGIC_NUMBERS[i]
            ) >> uint(64 - ROOK_OCCUPANCY_BITS[i])
            if ROOK_ATTACKS[i][magic_index] == uint(0):
                ROOK_ATTACKS[i][magic_index] = generate_rook_attacks(
                    i, fill_occupancy(uint(j), ROOK_OCCUPANCY[i])
                )
            elif ROOK_ATTACKS[i][magic_index] != generate_rook_attacks(
                i, fill_occupancy(uint(j), ROOK_OCCUPANCY[i])
            ):
                raise ValueError("Magic Number is not so magical!")
        for j in range(1 << BISHOP_OCCUPANCY_BITS[i]):
            magic_index = (
                fill_occupancy(uint(j), BISHOP_OCCUPANCY[i]) * BISHOP_MAGIC_NUMBERS[i]
            ) >> uint(64 - BISHOP_OCCUPANCY_BITS[i])
            if BISHOP_ATTACKS[i][magic_index] == uint(0):
                BISHOP_ATTACKS[i][magic_index] = generate_bishop_attacks(
                    i, fill_occupancy(uint(j), BISHOP_OCCUPANCY[i])
                )
            elif BISHOP_ATTACKS[i][magic_index] != generate_bishop_attacks(
                i, fill_occupancy(uint(j), BISHOP_OCCUPANCY[i])
            ):
                raise ValueError("Magic Number is not so magical!")


def generate_rook_moves(square, attack_mask):
    return ROOK_ATTACKS[square][
        (
            ((ROOK_OCCUPANCY[square] & attack_mask) * ROOK_MAGIC_NUMBERS[square])
            >> uint(64 - ROOK_OCCUPANCY_BITS[square])
        )
    ]


def generate_bishop_moves(square, attack_mask):
    return BISHOP_ATTACKS[square][
        (
            ((BISHOP_OCCUPANCY[square] & attack_mask) * BISHOP_MAGIC_NUMBERS[square])
            >> uint(64 - BISHOP_OCCUPANCY_BITS[square])
        )
    ]


def is_square_atacked(side, square, bitboards, board_data, black_pieces, white_pieces):
    if side  == 0:
        if bitboards[0] & BLACK_PAWN_ATTACKS[square]:
            return True
        elif bitboards[1] & KNIGHT_ATTACKS[square]:
            return True
        elif (bitboards[2] | bitboards[4]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> uint(64 - BISHOP_OCCUPANCY_BITS[square]))] & (~white_pieces):
            return True
        elif (bitboards[3] | bitboards[4]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> uint(64 - ROOK_OCCUPANCY_BITS[square]))] & (~white_pieces):
            return True
        elif bitboards[5] & KING_ATTACKS[square]:
            return True
    else:
        if bitboards[6] & WHITE_PAWN_ATTACKS[square]:
            return True
        elif bitboards[7] & KNIGHT_ATTACKS[square]:
            return True
        elif (bitboards[8] | bitboards[10]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> uint(64 - BISHOP_OCCUPANCY_BITS[square]))] & (~black_pieces):
            return True
        elif (bitboards[9] | bitboards[10]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> uint(64 - ROOK_OCCUPANCY_BITS[square]))] & (~black_pieces):
            return True
        elif bitboards[11] & KING_ATTACKS[square]:
            return True

    return False

def return_moves(side, bitboards, board_data):

    WHITE_PAWNS = bitboards[0]
    WHITE_KNIGHTS = bitboards[1]
    WHITE_BISHOPS = bitboards[2]
    WHITE_ROOKS = bitboards[3]
    WHITE_QUEEN = bitboards[4]
    WHITE_KING = bitboards[5]

    BLACK_PAWNS = bitboards[6]
    BLACK_KNIGHTS = bitboards[7]
    BLACK_BISHOPS = bitboards[8]
    BLACK_ROOKS = bitboards[9]
    BLACK_QUEEN = bitboards[10]
    BLACK_KING = bitboards[11]

    WHITE_PIECES = (
        WHITE_BISHOPS
        | WHITE_KING
        | WHITE_KNIGHTS
        | WHITE_PAWNS
        | WHITE_QUEEN
        | WHITE_ROOKS
    )

    BLACK_PIECES = (
        BLACK_BISHOPS
        | BLACK_KING
        | BLACK_KNIGHTS
        | BLACK_PAWNS
        | BLACK_QUEEN
        | BLACK_ROOKS
    )

    ALL_PIECES = BLACK_PIECES | WHITE_PIECES


    moves = zeros(218, dtype = uint32)      
    count = 0

    def add_move(source, target, piece, promoted, promoted_piece, enpassant, castling):
        nonlocal moves, count

        moves[count] = uint32(source) | uint32(target << 6) | uint32(piece << 12) | uint32(promoted << 16) | uint32(promoted_piece << 17) | uint32(enpassant << 19) | uint32(castling << 20) 
        count += 1


    if side == 0:


        while WHITE_PAWNS:
            curr_square = least_significant_bit_count(WHITE_PAWNS)
            WHITE_PAWNS ^= uint(1 << curr_square)
            attacks = WHITE_PAWN_ATTACKS[curr_square] & BLACK_PIECES

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks &= (attacks - uint(1))
                add_move(curr_square, to_square, 0, 0, 0, 0, 0)

            if uint(1 << (curr_square - 8) & ((1 << 64) - 1)) & (~ALL_PIECES):
                if 0 <= curr_square <= 7:
                    add_move(curr_square, curr_square - 8, 1, 1, 0, 0, 0)
                    add_move(curr_square, curr_square - 8, 1, 2, 0, 0, 0)
                    add_move(curr_square, curr_square - 8, 1, 3, 0, 0, 0)
                    add_move(curr_square, curr_square - 8, 1, 4, 0, 0, 0)

                elif 48 <= curr_square <= 55 and uint(1 << (curr_square - 16)) & (~ALL_PIECES):
                     add_move(curr_square, curr_square - 16, 0, 0, 0, 0, 0)

                else:
                    add_move(curr_square, curr_square - 8, 0, 0, 0, 0, 0)

            if board_data & uint32(1 << 5) and ((board_data >> uint32(6)) == curr_square - 9 or (board_data >> uint32(6)) == curr_square - 7) and not (uint32(1 << (board_data >> uint32(6))) & ALL_PIECES):
                add_move(curr_square, ((board_data >> uint32(6))), 0, 0, 0, 1, 0)


        while WHITE_KNIGHTS:
            curr_square = least_significant_bit_count(WHITE_KNIGHTS)
            WHITE_KNIGHTS ^= uint(1 << curr_square)
            attacks = KNIGHT_ATTACKS[curr_square] & BLACK_PIECES

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks &= (attacks - uint(1))
                add_move(curr_square, to_square, 1, 0, 0, 0, 0)
            
            moves_possible = KNIGHT_ATTACKS[curr_square] & (~ALL_PIECES)

            while moves_possible:
                to_square = least_significant_bit_count(moves_possible)
                moves_possible &= (moves_possible - uint(1))
                add_move(curr_square, to_square, 1, 0, 0, 0, 0)


        while WHITE_BISHOPS:
            curr_square = least_significant_bit_count(WHITE_BISHOPS)
            WHITE_BISHOPS ^= uint(1 << curr_square)
            attacks = BISHOP_ATTACKS[curr_square][
                (
                    (BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
                )
            ] & (~WHITE_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks &= (attacks - uint(1))
                add_move(curr_square, to_square, 2, 0, 0, 0, 0)

        while WHITE_ROOKS:
            curr_square = least_significant_bit_count(WHITE_ROOKS)
            WHITE_ROOKS ^= uint(1 << curr_square)
            attacks = ROOK_ATTACKS[curr_square][
                (
                    (ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
                )
            ] & (~WHITE_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks &= (attacks - uint(1))
                add_move(curr_square, to_square, 2, 0, 0, 0, 0)


                     

    '''               
    if BLACK_PAWNS & (uint(1) << uint(square)):
        res = BLACK_PAWN_ATTACKS[square] & WHITE_PIECES
        temp = BLACK_PAWN_PUSHES[square]
        while temp:
            index = least_significant_bit_count(temp)
            if not (uint(1) << uint(index)) & (BLACK_PIECES | WHITE_PIECES):
                res |= uint(1) << uint(index)
            else:
                break
            temp &= temp - uint(1)
        return res


    elif WHITE_PAWNS & (uint(1) << uint(square)):
        res = WHITE_PAWN_ATTACKS[square] & BLACK_PIECES
        temp = WHITE_PAWN_PUSHES[square]
        indices = []
        while temp:
            index = least_significant_bit_count(temp)
            indices.append(index)
            temp -= uint(1) << uint(index)
        for i in range(len(indices) - 1,-1,-1):
            index = indices[i]
            if not (uint(1) << uint(index)) & (BLACK_PIECES | WHITE_PIECES):
                res |= uint(1) << uint(index)
            else:
                break
        return res
    elif (BLACK_BISHOPS | WHITE_BISHOPS) & (uint(1) << uint(square)):
        moves = BISHOP_ATTACKS[square][
            (
                (
                    (BISHOP_OCCUPANCY[square] & (BLACK_PIECES | WHITE_PIECES))
                    * BISHOP_MAGIC_NUMBERS[square]
                )
                >> uint(64 - BISHOP_OCCUPANCY_BITS[square])
            )
        ]
        if BLACK_BISHOPS & (uint(1) << uint(square)):
            friendly_attacks = moves & BLACK_PIECES
        else:
            friendly_attacks = moves & WHITE_PIECES
        moves &= ~friendly_attacks
        return moves
    elif (BLACK_KNIGHTS | WHITE_KNIGHTS) & (uint(1) << uint(square)):
        moves = KNIGHT_ATTACKS[square]
        if BLACK_KNIGHTS & (uint(1) << uint(square)):
            friendly_attacks = moves & (BLACK_PIECES)
        else:
            friendly_attacks = moves & (WHITE_PIECES)
        moves &= ~friendly_attacks
        return moves
    elif (BLACK_ROOKS | WHITE_ROOKS) & (uint(1) << uint(square)):
        moves = ROOK_ATTACKS[square][
            (
                (
                    (ROOK_OCCUPANCY[square] & (BLACK_PIECES | WHITE_PIECES))
                    * ROOK_MAGIC_NUMBERS[square]
                )
                >> uint(64 - ROOK_OCCUPANCY_BITS[square])
            )
        ]
        if BLACK_ROOKS & (uint(1) << uint(square)):
            friendly_attacks = moves & BLACK_PIECES
        else:
            friendly_attacks = moves & WHITE_PIECES
        moves &= ~friendly_attacks
        return moves
    elif (BLACK_QUEEN | WHITE_QUEEN) & (uint(1) << uint(square)):
        rook_moves = ROOK_ATTACKS[square][
            (
                (
                    (ROOK_OCCUPANCY[square] & (BLACK_PIECES | WHITE_PIECES))
                    * ROOK_MAGIC_NUMBERS[square]
                )
                >> uint(64 - ROOK_OCCUPANCY_BITS[square])
            )
        ]
        bishop_moves = BISHOP_ATTACKS[square][
            (
                (
                    (BISHOP_OCCUPANCY[square] & (BLACK_PIECES | WHITE_PIECES))
                    * BISHOP_MAGIC_NUMBERS[square]
                )
                >> uint(64 - BISHOP_OCCUPANCY_BITS[square])
            )
        ]
        moves = rook_moves | bishop_moves
        if BLACK_QUEEN & (uint(1) << uint(square)):
            friendly_attacks = moves & BLACK_PIECES
        else:
            friendly_attacks = moves & WHITE_PIECES
        moves &= ~friendly_attacks
        return moves
    elif (BLACK_KING | WHITE_KING) & (uint(1) << uint(square)):
        moves = KING_ATTACKS[square]
        if BLACK_KING & (uint(1) << uint(square)):
            friendly_attacks = moves & BLACK_PIECES
        else:
            friendly_attacks = moves & WHITE_PIECES
        moves &= ~friendly_attacks
        return moves
    else:
        return uint(0)
    '''
    return trim_zeros(moves, 'b')


def print_moves(moves):
    for move in moves:
        print()
        print(f'From: {square_string[move & uint32((1 << 6) - 1)]}')
        print(f'To: {square_string[(move >> uint32(6)) & uint32((1 << 6) - 1)]}')
        print(f'Piece: {piece_string[(move >> uint32(12)) & uint32((1 << 4) - 1)]}')
        print(f'Promotion: {"No" if not ((move >> uint32(16)) & uint32(1)) else piece_string[(move >> uint32(17)) & (uint32((1 << 4) - 1))]}')
        print(f'EnPassant: {"Yes" if ((move >> uint32(19)) & uint32(1)) else "No"}')
        print(f'Castling: {"Yes" if ((move >> uint32(20)) & uint32(1)) else "No"}')

def make_move(bitboards,from_,to,data):
    # bitboards format: list[P,N,B,R,Q,K,p,n,b,r,q,k]
    # from_,to: tuple(row,col)
    # data: uint64 (format for data given below this fn)
    pass

"""
BOARD REPRESENTATION
12 bitboards for positions in order of 'PNBRQKpnbrqk'

13 32 bit integer

first bit = 0 if white to play 1 if black to play
next four bits for castling data = KQkq
next bit = enpassant possible or not
next 6 bits = enpassant square
"""


def print_chess_board(boards, board_data):
    c = uint(0)
    
    for i in range(8):
        print(8 - i, '    ', end ='')
        for j in range(8):
            for k in range(12):
                if boards[k] & (uint(1) << c):
                    print(f'{piece_string[k]}   ', end = '')
            c += uint(1)
        print('\n')
    print()        
    print('      A   B   C   D   E   F   G   H')
    print()
    print(f'Castling rights: {"K" if ((board_data << uint32(1)) & uint32(1)) else "-"}{"Q" if ((board_data << uint32(2)) & uint32(1)) else "-"}{"k" if ((board_data << uint32(3)) & uint32(1)) else "-"}{"q" if ((board_data << uint32(4)) & uint32(1)) else "-"}')
    print()
    print(f'Side to move: {"Black" if (board_data & uint32(1)) else "White"}')
    print()
    print(f'En Passant: {"Not possible" if (board_data & uint32(1 << 5)) else square_string[((board_data << uint32(6)) & (uint32(1 << 6) - 1))]}')
    print('\n')



bitboards = array(BITBOARDS.copy())
board_data = data

moves = return_moves(0, bitboards, board_data)

print_moves(moves)

print_chess_board(bitboards, board_data)