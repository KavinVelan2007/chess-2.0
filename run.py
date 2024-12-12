from GUI.Account import Account

def run():

    a = Account()
    a.mainloop()

if __name__ == '__main__':

    run()

"""from fen import *
from zobrist import ComputeHash

bitboards,data = generate_bitboards_from_board(fenString)

import pickle

with open('chess-2.0/zobristtable.bin','rb') as f:

    table = pickle.load(f)

bitboards,boarddata = generate_bitboards_from_board(fenString)

import time
a = time.time()
print(ComputeHash(bitboards,table))
print(time.time() - a)"""