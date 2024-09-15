from pickle import NONE
from numpy import uint64 as uint, uint32
import time
import random
random.seed(time.time())
from data import * 

def print_bitboard(bit_board):
    c = uint(0)
    
    for i in range(8):
        print(8 - i, '    ', end ='')
        for j in range(8):
            print('1   ' if bit_board & (uint(1) << c) else '.   ', end = '')
            c += uint(1)
        print('\n')
    print()        
    print('      A   B   C   D   E   F   G   H')
    print()
    print('BitBoard Value:', bit_board)
    print('\n')


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

def generate_bishop_occupancy():
    for i in range(64):
        n = uint(0)
        r,c = i // 8,i % 8
        row,col = r + 1,c + 1
        while row <= 6 and col <= 6:
            n |= uint(1) << uint(row * 8 + col)
            row += 1
            col += 1
        row,col = r - 1,c + 1
        while row >= 1 and col <= 6:
            n |= uint(1) << uint(row * 8 + col)
            row -= 1
            col += 1
        row,col = r + 1,c - 1
        while row <= 6 and col >= 1:
            n |= uint(1) << uint(row * 8 + col)
            row += 1
            col -= 1
        row,col = r - 1,c - 1
        while row >= 1 and col >= 1:
            n |= uint(1) << uint(row * 8 + col)
            row -= 1
            col -= 1
        print(f'uint({n})',end=',')

def count_bits(bit_board):
    c = 0
    while bit_board:
        bit_board &= bit_board - uint(1)
        c += 1
    return c


def least_significant_bit_count(bit_board):
    return(count_bits(bit_board - uint(1)) - count_bits(bit_board) + 1)


def fill_occupancy(value, bit_board):
    occupancy = uint(0)
    c = uint(0)
    while bit_board:
        if value & (uint(1) << c):
            occupancy |= uint(1) << uint(count_bits(bit_board - uint(1)) - count_bits(bit_board) + uint(1))
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
    return ((uint(rand() & uint32(0xFFFF))) | (uint(rand() & uint32(0xFFFF)) << uint(16)) | (uint(rand() & uint32(0xFFFF)) << uint(32)) | (uint(rand() & uint32(0xFFFF)) << uint(48)))


def generate_bishop_attacks(i,mask):
    n = uint(0)
    r,c = i // 8,i % 8
    row,col = r + 1,c + 1
    while row <= 7 and col <= 7:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row += 1
        col += 1
    row,col = r - 1,c + 1
    while row >= 0 and col <= 7:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row -= 1
        col += 1
    row,col = r + 1,c - 1
    while row <= 7 and col >= 0:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row += 1
        col -= 1
    row,col = r - 1,c - 1
    while row >= 0 and col >= 0:
        n |= uint(1) << uint(row * 8 + col)
        if mask & (uint(1) << uint(row * 8 + col)):
            break
        row -= 1
        col -= 1
    return n

def generate_rook_attacks(i,mask):
    row = i // 8
    col = i % 8
    n = uint(0)
    for r in range(row + 1,8):
        n |= uint(1) << uint(r * 8 + col)
        if mask & (uint(1) << uint(r * 8 + col)):
            break
    for r in range(row - 1,-1,-1):
        n |= uint(1) << uint(r * 8 + col)
        if mask & (uint(1) << uint(r * 8 + col)):
            break
    for c in range(col + 1,8):
        n |= uint(1) << uint(row * 8 + c)
        if mask & (uint(1) << uint(row * 8 + c)):
            break
    for c in range(col - 1,-1,-1):
        n |= uint(1) << uint(row * 8 + c)
        if mask & (uint(1) << uint(row * 8 + c)):
            break
    return n


def generate_magic_numbers(position, bits_present, piece): # For the piece parameter, bishop = 0, rook = 1
    occupancy = []
    attack = []
    used_attacks = []
    current_occupancy = ROOK_OCCUPANCY[position] if piece else BISHOP_OCCUPANCY[position]
    for i in range(uint(1) << uint(bits_present)):
        occupancy += [fill_occupancy(uint(i), current_occupancy)]
        attack += [generate_rook_attacks(position, occupancy[i]) if piece else generate_bishop_attacks(position, occupancy[i])]
        
    for i in range(100000000):
        magic_number = uint(random.randint(0, (1 << 64) - 1)) & uint(random.randint(0, (1 << 64) - 1))   
        if count_bits((current_occupancy * magic_number) & uint(0xFF00000000000000)) < 6:
            continue
        used_attacks = [uint(0) for i in range(uint(1) << uint(bits_present))]
        
        index = 0
        failed = False
        
        while not failed and index < (uint(1) << uint(bits_present)):
            magic_index = ((occupancy[index] * magic_number) >> uint(64 - bits_present))
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
    ROOK_ATTACKS = []
    BISHOP_ATTACKS = []
    for i in range(64):
        ROOK_ATTACKS += [[uint(0) for x in range(1 << ROOK_OCCUPANCY_BITS[i])]]
        BISHOP_ATTACKS += [[uint(0) for x in range(1 << BISHOP_OCCUPANCY_BITS[i])]]
        for j in range(1 << ROOK_OCCUPANCY_BITS[i]):
            magic_index = ((fill_occupancy(uint(j), ROOK_OCCUPANCY[i]) * ROOK_MAGIC_NUMBERS[i]) >> uint(64 - ROOK_OCCUPANCY_BITS[i]))
            ROOK_ATTACKS[i][magic_index] = generate_rook_attacks(i, fill_occupancy(uint(j), ROOK_OCCUPANCY[i]))
        for j in range(1 << BISHOP_OCCUPANCY_BITS[i]):
            magic_index = ((fill_occupancy(uint(j), BISHOP_OCCUPANCY[i]) * BISHOP_MAGIC_NUMBERS[i]) >> uint(64 - BISHOP_OCCUPANCY_BITS[i]))
            BISHOP_ATTACKS[i][magic_index] = generate_bishop_attacks(i, fill_occupancy(uint(j), BISHOP_OCCUPANCY[i]))


def generate_rook_moves(square, attack_mask):
    return ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & attack_mask) * ROOK_MAGIC_NUMBERS[square]) >> uint(64 - ROOK_OCCUPANCY_BITS[square]))]


def generate_bishop_moves(square, attack_mask):
    return BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & attack_mask) * BISHOP_MAGIC_NUMBERS[square]) >> uint(64 - BISHOP_OCCUPANCY_BITS[square]))]