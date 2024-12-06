"""from GUI.Main import Game

from fen import *

with open("FENString.txt", "r"):

    BitBoards, BoardData = generate_bitboards_from_board(fenString)

MainGame = Game(BitBoards=BitBoards, BoardData=BoardData)
"""
# from brains import *

# perft()


from GUI.Account import Account

a = Account()
a.mainloop()


"""from brains import perft # type: ignore

perft(int(input('Enter Depth: ')))
"""