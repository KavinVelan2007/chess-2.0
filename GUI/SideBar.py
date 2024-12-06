import customtkinter as ctk
import brains
from fen import *
from PIL import Image
from GUI.Preferences import Preferences
import brains
from fen import generate_bitboards_from_board

ctk.set_default_color_theme("GUI\\Themes.json")

class SideBar(ctk.CTkFrame):


    def __init__(self, ParentObject):

        self.ParentObject = ParentObject

        super().__init__(self.ParentObject)

        self.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure((3, ), weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.Fen = ctk.StringVar()

        self.LogoLabel = ctk.CTkLabel(
            self, text="Chess", font=ctk.CTkFont(size=25, weight="bold"))

        self.LogoLabel.grid(row=0, column=0, padx=30, pady=20)

        self.NewGameButton = ctk.CTkButton(
            self, text="➕  New Game", height=30, anchor="center", command=self.StartNewGame)

        self.NewGameButton.grid(row=1, column=0, ipadx=10, ipady=10, pady=20)

        photo = Image.open("GUI\\Resources\\Misc\\SaveIcon.png")

        self.SaveQuitButton = ctk.CTkButton(self, height=25, command=self.CopyFENToClipboard, text="Save Progress", image=ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(25, 25)), anchor="center")

        self.SaveQuitButton.image = ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(25, 25))

        self.SaveQuitButton.grid(row=2, column=0, ipadx=10, ipady=10, pady=20)

        photo = Image.open("GUI\\Resources\\Misc\\AppearanceModeIcon.png")

        self.AppeareceModeLabel = ctk.CTkLabel(self, font=ctk.CTkFont(size=20), text=" Appearance Mode", anchor="center", image=ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(30, 30)), compound="left")

        self.AppeareceModeLabel.image = ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(30, 30))

        self.AppeareceModeLabel.grid(
            row=4, column=0, ipadx=10, ipady=10, padx=20, pady=10, sticky="s")
        
        self.OpponentMode = ctk.CTkOptionMenu(
            self, height=40, width=200, values=["Human","Bot"], command=self.SwitchToAIMode
        )

        self.OpponentMode.grid(row=3,column=0,pady=50)

        self.AppeareceModeDropDown = ctk.CTkOptionMenu(
            self, height=40, width=200, values=["System", "Light", "Dark"], command=self.ChangeAppearanceMode)

        self.AppeareceModeDropDown.grid(row=5, column=0, pady=(10, 50))

        self.ScalingLabel = ctk.CTkLabel(self, font=ctk.CTkFont(
            size=20), text=" Scaling", anchor="center")

        self.ScalingLabel.grid(row=6, column=0, pady=10)

        self.ScalingMenu = ctk.CTkOptionMenu(self, width=200, height=40, values=[
                                             "75%", "80%", "90%", "100%", "110%", "120%", "125%"], command=self.ChangeScaling)

        self.ScalingMenu.grid(row=7, column=0, pady=(10, 50))

        self.ScalingMenu.set("100%")

        self.PreferencesButton = ctk.CTkButton(self, text="Preferences", command=self.showPreferences, height=30, anchor="center", image=ctk.CTkImage(light_image=Image.open(
            "GUI\\Resources\\Misc\\PreferencesIcon.png"), dark_image=Image.open("GUI\\Resources\\Misc\\PreferencesIcon.png"), size=(30, 30)), compound="left")

        self.PreferencesButton.grid(
            row=8, column=0, ipadx=10, ipady=10, pady=20)
        
    def showPreferences(self):

        Preferences(self.ParentObject).show()

    def CopyFENToClipboard(self):

        BitBoards, BoardData = self.ParentObject.ChessBoardObj.bitboards, self.ParentObject.ChessBoardObj.board_data

        from fen import convert_bitboards_to_fen

        import pyperclip

        from tkinter import messagebox

        # rnbq1rk1/pppp2pp/5n2/4pp2/1BPP4/8/PPQ1PPPP/RN2KBNR w kq - 0 0
        # rn2kbnr/ppq1pppp/8/1bpp4/4PP2/5N2/PPPP2PP/RNBQ1RK1 w kq - 0 6

        fen = convert_bitboards_to_fen(BitBoards,BoardData)

        pyperclip.copy(fen)

        messagebox.showinfo('FEN Copied','The FEN Notation has been added to your Clip Board')

    def ChangeScaling(self, ScalingValue):

        ctk.set_widget_scaling(
            int(ScalingValue.replace('%', '')) / 100)


    def ChangeAppearanceMode(self, AppearanceMode):

        ctk.set_appearance_mode(AppearanceMode)

        ctk.AppearanceModeTracker.update()

        self.ParentObject.BaseColour = (26, 26, 26) if ctk.get_appearance_mode() == "Dark" else (242, 242, 242)

    def StartNewGame(self):
        if self.Fen.get():

            BitBoards,BoardData = generate_bitboards_from_board(self.Fen.get())

            self.ParentObject.ChessBoardObj = brains.Board(BitBoards,BoardData)
            print(BoardData)
            
            self.ParentObject.BitBoards = self.ParentObject.ChessBoardObj.bitboards
            self.ParentObject.BoardData = self.ParentObject.ChessBoardObj.board_data

            self.ParentObject.ValidMoves = self.ParentObject.ChessBoardObj.ReturnMoves()

            self.ParentObject.Turn = self.Fen.get().split()[1].upper()

            print('yes')

        else:

            self.ParentObject.Turn = 'W'

            with open("FENString.txt", "r"):

                BitBoards, BoardData = generate_bitboards_from_board(fenString)

            self.ParentObject.ChessBoardObj = brains.Board(BitBoards,BoardData)

            print(BoardData)

            self.ParentObject.BitBoards = self.ParentObject.ChessBoardObj.bitboards
            self.ParentObject.BoardData = self.ParentObject.ChessBoardObj.board_data

            self.ParentObject.ValidMoves = self.ParentObject.ChessBoardObj.ReturnMoves()

            self.ParentObject.CurrentSquare = None

            print('yes')

    def SwitchToAIMode(self, Mode):

        if Mode == 'Bot':

            self.ParentObject.AgainstAI = True
        
        else:

            self.ParentObject.AgainstAI = False

        self.StartNewGame()

        self.ParentObject.CurrentSquare = None