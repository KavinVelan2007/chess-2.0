from numpy import uint64 as uint, uint32, array, zeros, trim_zeros
import time
import os
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

            if 8 <= curr_square <= 15:

                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks &= (attacks - uint(1))
                    add_move(curr_square, to_square, 0, 1, 0, 0, 0)
                    add_move(curr_square, to_square, 0, 1, 1, 0, 0)
                    add_move(curr_square, to_square, 0, 1, 2, 0, 0)
                    add_move(curr_square, to_square, 0, 1, 3, 0, 0)

                if uint(1 << (curr_square - 8)) & (~ALL_PIECES):
                    add_move(curr_square, curr_square - 8, 0, 1, 0, 0, 0)
                    add_move(curr_square, curr_square - 8, 0, 1, 1, 0, 0)
                    add_move(curr_square, curr_square - 8, 0, 1, 2, 0, 0)
                    add_move(curr_square, curr_square - 8, 0, 1, 3, 0, 0)

                
            else:

                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= uint(1 << to_square)
                    add_move(curr_square, to_square, 0, 0, 0, 0, 0)

                if uint(1 << (curr_square - 8)) & (~ALL_PIECES):

                    if 48 <= curr_square <= 55 and uint(1 << (curr_square - 16)) & (~ALL_PIECES):
                        add_move(curr_square, curr_square - 8, 0, 0, 0, 0, 0)
                        add_move(curr_square, curr_square - 16, 0, 0, 0, 0, 0)

                    else:
                        add_move(curr_square, curr_square - 8, 0, 0, 0, 0, 0)

                if (board_data & uint32(1 << 5)) and (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == (curr_square - 9) or (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == curr_square - 7)):
                    add_move(curr_square, ((board_data >> uint32(6) & uint32((1 << 6) - 1))), 0, 0, 0, 1, 0)


        while WHITE_KNIGHTS:
            curr_square = least_significant_bit_count(WHITE_KNIGHTS)
            WHITE_KNIGHTS ^= uint(1 << curr_square)
            
            moves_possible = KNIGHT_ATTACKS[curr_square] & (~WHITE_PIECES)

            while moves_possible:
                to_square = least_significant_bit_count(moves_possible)
                moves_possible ^= uint(1 << to_square)
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
                attacks ^= uint(1 << to_square)
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
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 3, 0, 0, 0, 0)


        while WHITE_QUEEN:
            curr_square = least_significant_bit_count(WHITE_QUEEN)
            WHITE_QUEEN^= uint(1 << curr_square)
            attacks = BISHOP_ATTACKS[curr_square][
                (
                    (BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
                )
            ] & (~WHITE_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 4, 0, 0, 0, 0)

            attacks = ROOK_ATTACKS[curr_square][
                (
                    (ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
                )
            ] & (~WHITE_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 4, 0, 0, 0, 0)

        while WHITE_KING:
            curr_square = least_significant_bit_count(WHITE_KING)
            WHITE_KING ^= uint(1 << curr_square)
            attacks = KING_ATTACKS[curr_square] & (~WHITE_PIECES)
            
            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 5, 0, 0, 0, 0)

            if board_data & uint32(2) and not (ALL_PIECES & uint((1 << 62) + (1 << 61))) and not is_square_atacked(1, 61, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not is_square_atacked(1, 60, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
                add_move(curr_square, 62, 5, 0, 0, 0, 1)

            if board_data & uint32(4) and not (ALL_PIECES & uint((1 << 59) + (1 << 58) + (1 << 57))) and not is_square_atacked(1, 59, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not is_square_atacked(1, 60, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
                add_move(curr_square, 58, 5, 0, 0, 0, 1)



    else:


        while BLACK_PAWNS:
            curr_square = least_significant_bit_count(BLACK_PAWNS)
            BLACK_PAWNS ^= uint(1 << curr_square)
            attacks = BLACK_PAWN_ATTACKS[curr_square] & WHITE_PIECES

            if 56 <= curr_square <= 63:

                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= uint(1 << to_square)
                    add_move(curr_square, to_square, 6, 1, 0, 0, 0)
                    add_move(curr_square, to_square, 6, 1, 1, 0, 0)
                    add_move(curr_square, to_square, 6, 1, 2, 0, 0)
                    add_move(curr_square, to_square, 6, 1, 3, 0, 0)

                if uint(1 << (curr_square + 8)) & (~ALL_PIECES):
                    add_move(curr_square, curr_square + 8, 6, 1, 0, 0, 0)
                    add_move(curr_square, curr_square + 8, 6, 1, 1, 0, 0)
                    add_move(curr_square, curr_square + 8, 6, 1, 2, 0, 0)
                    add_move(curr_square, curr_square + 8, 6, 1, 3, 0, 0)

            else:

                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= uint(1 << to_square)
                    add_move(curr_square, to_square, 6, 0, 0, 0, 0)

                if uint(1 << (curr_square + 8)) & (~ALL_PIECES):

                    if 8 <= curr_square <= 15 and uint(1 << (curr_square + 16)) & (~ALL_PIECES):
                        add_move(curr_square, curr_square + 8, 6, 0, 0, 0, 0)
                        add_move(curr_square, curr_square + 16, 6, 0, 0, 0, 0)

                    else:
                        add_move(curr_square, curr_square + 8, 6, 0, 0, 0, 0)

                if (board_data & uint32(1 << 5)) and (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == (curr_square + 9) or (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == curr_square + 7)):
                    add_move(curr_square, ((board_data >> uint32(6) & uint32((1 << 6) - 1))), 6, 0, 0, 1, 0)


        while BLACK_KNIGHTS:
            curr_square = least_significant_bit_count(BLACK_KNIGHTS)
            BLACK_KNIGHTS ^= uint(1 << curr_square)
            
            moves_possible = KNIGHT_ATTACKS[curr_square] & (~BLACK_PIECES)

            while moves_possible:
                to_square = least_significant_bit_count(moves_possible)
                moves_possible ^= uint(1 << to_square)
                add_move(curr_square, to_square, 7, 0, 0, 0, 0)


        while BLACK_BISHOPS:
            curr_square = least_significant_bit_count(BLACK_BISHOPS)
            BLACK_BISHOPS ^= uint(1 << curr_square)
            attacks = BISHOP_ATTACKS[curr_square][
                (
                    (BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
                )
            ] & (~BLACK_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 8, 0, 0, 0, 0)


        while BLACK_ROOKS:
            curr_square = least_significant_bit_count(BLACK_ROOKS)
            BLACK_ROOKS ^= uint(1 << curr_square)
            attacks = ROOK_ATTACKS[curr_square][
                (
                    (ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
                )
            ] & (~BLACK_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 9, 0, 0, 0, 0)


        while BLACK_QUEEN:
            curr_square = least_significant_bit_count(BLACK_QUEEN)
            BLACK_QUEEN^= uint(1 << curr_square)
            attacks = BISHOP_ATTACKS[curr_square][
                (
                    (BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
                )
            ] & (~BLACK_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 10, 0, 0, 0, 0)

            attacks = ROOK_ATTACKS[curr_square][
                (
                    (ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
                    >> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
                )
            ] & (~BLACK_PIECES)

            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 10, 0, 0, 0, 0)

        while BLACK_KING:
            curr_square = least_significant_bit_count(BLACK_KING)
            BLACK_KING ^= uint(1 << curr_square)
            attacks = KING_ATTACKS[curr_square] & (~BLACK_PIECES)
            
            while attacks:
                to_square = least_significant_bit_count(attacks)
                attacks ^= uint(1 << to_square)
                add_move(curr_square, to_square, 11, 0, 0, 0, 0)

            if board_data & uint32(8) and not (ALL_PIECES & uint((1 << 5) + (1 << 6))) and not is_square_atacked(0, 3, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not is_square_atacked(0, 4, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
                add_move(curr_square, 6, 11, 0, 0, 0, 1)

            if board_data & uint32(16) and not (ALL_PIECES & uint((1 << 1) + (1 << 2) + (1 << 3))) and not is_square_atacked(0, 4, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not is_square_atacked(0, 5, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
                add_move(curr_square, 2, 11, 0, 0, 0, 1)



    return trim_zeros(moves, 'b')


def print_moves(moves):
    for move in moves:
        print()
        print(f'From: {square_string[move & uint32((1 << 6) - 1)]}')
        print(f'To: {square_string[(move >> uint32(6)) & uint32((1 << 6) - 1)]}')
        print(f'Piece: {piece_string[(move >> uint32(12)) & uint32((1 << 4) - 1)]}')
        print(f'Promotion: {"No" if not ((move >> uint32(16)) & uint32(1)) else piece_string[(move >> uint32(17)) & (uint32((1 << 4) - 1)) + 1 + (((move >> uint32(12)) & uint32((1 << 4) - 1)) // uint32(6) * 6)]}')
        print(f'EnPassant: {"Yes" if ((move >> uint32(19)) & uint32(1)) else "No"}')
        print(f'Castling: {"Yes" if ((move >> uint32(20)) & uint32(1)) else "No"}')

def make_move(move, bitboards, data):
    # bitboards format: list[P,N,B,R,Q,K,p,n,b,r,q,k]
    # from_,to: tuple(row,col)
    # data: uint64 (format for data given below this fn)
    piece = (move >> uint32(12)) & uint32(15)
    source = move & uint32(63)
    target = (move >> uint32(6)) & uint32(63)

    if ((data << uint32(12)) & uint32(63)) == 100:
        return False

    if 0 <= piece <= 5:
        
        if (move >> uint32(16)) & uint32(1):
            bitboards[0] ^= uint(1 << source)
            bitboards[((move >> uint32(17)) & uint32(3)) + 1] |= uint(1 << target)
            data &= uint32(4095)

        elif (move << uint32(19)) & uint32(1):
            bitboards[0] ^= uint((1 << source) + (1 << target))
            bitboards[6] ^= uint(1 << (target + 8))
            data &= uint32(4095)

        elif (move << uint32(19)) & uint32(1):
            bitboards[5] ^= uint((1 << source) + (1 << target))
            bitboards[3] ^= uint(1 << ((source + target) // 2))

            if target == 62:
                bitboards[3] ^= uint(1 << 63)
            
            else:
                bitboards[3] ^= uint(1 << 56)

            data += uint32(4096)

        else:
            bitboards[piece] ^= uint((1 << source) + (1 << target))

            mask = uint(0)
            for i in range(6):
                mask |= bitboards[6 + i]
                bitboards[i + 6] &= ~uint(1 << target)

            if mask & uint(1 << target):
                data &= uint32(4095)
            else:
                data += uint32(4096)

        data |= uint32(1)

        if piece == 0 and source - target == 16:
            data &= ~uint32(((1 << 6) - 1) << 6)
            data |= uint32((target + 8) << 6)

        if piece == 5:
            data &= ~uint32(6)

        if data & uint32(2) and piece == 3 and source == 63:
            data &= ~uint32(2)

        elif data & uint32(4) and piece == 3 and source == 56:
            data &= ~uint32(4)

        if is_square_atacked(1, least_significant_bit_count(bitboards[5]), bitboards, data, bitboards[6] | bitboards[7] | bitboards[8] | bitboards[9] | bitboards[10] | bitboards[11], bitboards[0] | bitboards[1] | bitboards[2] | bitboards[3] | bitboards[4] | bitboards[5]):
            return False

    else:
        if (move >> uint32(16)) & uint32(1):
            bitboards[6] ^= uint(1 << source)
            bitboards[((move >> uint32(17)) & uint32(3)) + 7] |= uint(1 << target)
            data &= uint32(4095)

        elif (move << uint32(19)) & uint32(1):
            bitboards[6] ^= uint((1 << source) + (1 << target))
            bitboards[0] ^= uint(1 << (target + 8))
            data &= uint32(4095)

        elif (move << uint32(19)) & uint32(1):
            bitboards[11] ^= uint((1 << source) + (1 << target))
            bitboards[9] ^= uint(1 << ((source + target) // 2))

            if target == 2:
                bitboards[9] ^= uint(1 << 3)
            
            else:
                bitboards[9] ^= uint(1 << 5)

        else:
            bitboards[piece] ^= uint((1 << source) + (1 << target))

            mask = uint(0)
            for i in range(6):
                mask |= bitboards[i]
                bitboards[i] &= ~uint(1 << target)

            if mask & uint(1 << target):
                data &= uint32(4095)
            else:
                data += uint32(4096)

        data ^= uint32(1)

        if piece == 6 and target - source == 16:
            data &= ~uint32(((1 << 6) - 1) << 6)
            data |= uint32((target - 8) << 6)

        if piece == 11:
            data &= ~uint32(24)

        if data & uint32(8) and piece == 9 and source == 7:
            data &= ~uint32(8)

        elif data & uint32(16) and piece == 9 and source == 0:
            data &= ~uint32(16)

        if is_square_atacked(0, least_significant_bit_count(bitboards[11]), bitboards, data, bitboards[6] | bitboards[7] | bitboards[8] | bitboards[9] | bitboards[10] | bitboards[11], bitboards[0] | bitboards[1] | bitboards[2] | bitboards[3] | bitboards[4] | bitboards[5]):
            return False

    return bitboards, data
    

"""
BOARD REPRESENTATION
12 bitboards for positions in order of 'PNBRQKpnbrqk'

13 32 bit integer

first bit = 0 if white to play 1 if black to play
next four bits for castling data = KQkq
next bit = enpassant possible or not
next 6 bits = enpassant square
next 6 bits = half move clock
"""


def print_chess_board(boards, board_data):
    c = uint(0)
    
    for i in range(8):
        print(8 - i, '    ', end ='')
        for j in range(8):
            for k in range(12):
                if boards[k] & (uint(1) << c):
                    print(f'{piece_string[k]}   ', end = '')
                    break
            else:
                print('    ', end = '')
            c += uint(1)
        print('\n')
    print()        
    print('      A   B   C   D   E   F   G   H')
    print()
    print(f'Side to move: {"Black" if (board_data & uint32(1)) else "White"}')
    print()
    print(f'Castling rights: {"K" if ((board_data >> uint32(1)) & uint32(1)) else "-"}{"Q" if ((board_data >> uint32(2)) & uint32(1)) else "-"}{"k" if ((board_data >> uint32(3)) & uint32(1)) else "-"}{"q" if ((board_data >> uint32(4)) & uint32(1)) else "-"}')
    print()
    print(f'En Passant: {"Not possible" if not (board_data & uint32(1 << 5)) else square_string[((board_data >> uint32(6)) & (uint32(1 << 6) - 1))]}')
    print()
    print(f'Half Moves: {(board_data >> uint32(12)) & (uint32((1 << 6 )- 1))}')
    print()
    print('Board Data:', bin(board_data))
    print('\n')


def perft(depth, bitboards, board_data, nodes):
    if depth == 0:
        nodes += 1

    else:

        moves = return_moves(board_data & uint32(1), bitboards, board_data)

        for move in moves:
            moved = make_move(move, bitboards.copy(), board_data)

            if moved == False:
                continue

            else:
                temp_bitboards, temp_board_data = moved

            perft(depth - 1, temp_bitboards, temp_board_data, nodes)



bitboards = array(BITBOARDS.copy())
board_data = data



moves = return_moves(0, bitboards, board_data)
'''
for move in moves:
    a = make_move(move, bitboards.copy(), board_data)
    if a == False:
        continue
    else:
        temp_bitboards, temp_board_data = a

    moves2 = return_moves(1, temp_bitboards, temp_board_data)

    for move2 in moves2:
        b = make_move(move2, temp_bitboards.copy(), temp_board_data)
        if b == False:
            continue
        else:
            temp_temp_bitboards, temp_temp_board_data = b
        print_chess_board(temp_temp_bitboards, temp_temp_board_data)
        input()
'''


def count_bits(bit_board):
    c = 0
    while bit_board:
        bit_board &= bit_board - uint(1)
        c += 1
    return c

def least_significant_bit_count(bit_board):
    return int(bit_board).bit_length() - 1

nodes = array(0)
stime = time.time()
#print(stime)
perft(4, bitboards, board_data, nodes)
os.system('cls')

print(int(least_significant_bit_count(bitboards[3])))

print(nodes)
print(time.time() - stime)