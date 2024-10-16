from GUI.GUIMain import Game

from fen import *

with open("FENString.txt", "r"):

    BitBoards, BoardData = generate_bitboards_from_board(fenString)

MainGame = Game(BitBoards=BitBoards, BoardData=BoardData)

MainGame.MainLoop()

import os

os.system('cls')