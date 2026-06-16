from GUI.Defaults import (
    DEFAULT_BOARD_THEME,
    DEFAULT_GUEST_USERNAME,
    DEFAULT_PIECE_THEME,
)
from GUI.Main import Game
from fen import fenString, generate_bitboards_from_board


def run():
    BitBoards, BoardData = generate_bitboards_from_board(fenString)
    Game(
        BitBoards=BitBoards,
        BoardData=BoardData,
        username=DEFAULT_GUEST_USERNAME,
        piece_preference=DEFAULT_PIECE_THEME,
        board_preference=DEFAULT_BOARD_THEME,
        store_preferences=False,
    )

if __name__ == '__main__':
    run()
