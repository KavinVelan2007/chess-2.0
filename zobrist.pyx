import pickle
from numpy import uint64 as uint
from fen import *
import random
cimport cython

ctypedef (unsigned long long) U64
ctypedef (unsigned int) U32

def InitTable():

    cdef U64[8][8][12] ZobristTable = [[[random.randint(0, 2 ** 64) for _ in range(12)] for i in range(8)] for j in range(8)]

    with open('zobristtable.bin','wb') as file:

        pickle.dump(ZobristTable, file)

cdef ComputeHashInt(bitboards, table):

    cdef U64 hash = 0
    cdef int i = 0
    cdef U64 bitboard
    cdef int row
    cdef int col

    for i, bitboard in enumerate(bitboards):

        for row in range(8):

            for col in range(8):

                if uint(bitboard) & (uint(1) << uint(row * 8 + col)):

                    hash ^= table[row][col][i]

    return hash

cpdef ComputeHash(bitboards, table):

    return ComputeHashInt(bitboards, table)