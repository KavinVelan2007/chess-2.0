import pickle
from numpy import uint64 as uint
from fen import *
import random

def InitTable():

    ZobristTable = [[[random.randint(0, 2 ** 64) for _ in range(12)] for i in range(8)] for j in range(8)]

    with open('zobristtable.bin','wb') as file:

        pickle.dump(ZobristTable, file)

def ComputeHash(bitboards, table):

    hash = 0

    for i, bitboard in enumerate(bitboards):

        for row in range(8):

            for col in range(8):

                if uint(bitboard) & (uint(1) << uint(row * 8 + col)):

                    hash ^= table[row][col][i]

    return hash

with open('chess-2.0/zobristtable.bin','rb') as file:

    table = pickle.load(file)

bitboards, boarddata = generate_bitboards_from_board(fenString)

print(ComputeHash(bitboards, table))
