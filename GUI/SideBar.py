import customtkinter as ctk
from fen import *
from PIL import Image
from GUI.Preferences import Preferences
import brains
from tkinter import messagebox


ctk.set_default_color_theme("chess-2.0\\GUI\\Themes.json")


class SideBar(ctk.CTkFrame):

    def __init__(self, ParentObject):
        self.ParentObject = ParentObject
        super().__init__(self.ParentObject)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure((3,), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.Fen = ctk.StringVar()
        self.LogoLabel = ctk.CTkLabel(
            self, text="Chess", font=ctk.CTkFont(size=25, weight="bold")
        )
        self.LogoLabel.grid(row=0, column=0, padx=30, pady=20)
        self.NewGameButton = ctk.CTkButton(
            self,
            text="➕  New Game",
            height=30,
            anchor="center",
            command=self.StartNewGame,
        )
        self.NewGameButton.grid(row=1, column=0, ipadx=10, ipady=10, pady=20)
        photo = Image.open("chess-2.0\\GUI\\Resources\\Misc\\SaveIcon.png")
        self.SaveQuitButton = ctk.CTkButton(
            self,
            height=25,
            command=self.CopyFENToClipboard,
            text="Save Progress",
            image=ctk.CTkImage(
                light_image=photo, dark_image=photo, size=(25, 25)
            ),
            anchor="center",
        )
        self.SaveQuitButton.image = ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(25, 25)
        )
        self.SaveQuitButton.grid(row=2, column=0, ipadx=10, ipady=10, pady=20)
        photo = Image.open(
            "chess-2.0\\GUI\\Resources\\Misc\\AppearanceModeIcon.png"
        )
        self.AppeareceModeLabel = ctk.CTkLabel(
            self,
            font=ctk.CTkFont(size=20),
            text=" Appearance Mode",
            anchor="center",
            image=ctk.CTkImage(
                light_image=photo, dark_image=photo, size=(30, 30)
            ),
            compound="left",
        )
        self.AppeareceModeLabel.image = ctk.CTkImage(
            light_image=photo, dark_image=photo, size=(30, 30)
        )
        self.AppeareceModeLabel.grid(
            row=4, column=0, ipadx=10, ipady=10, padx=20, pady=10, sticky="s"
        )
        self.OpponentMode = ctk.CTkOptionMenu(
            self,
            height=40,
            width=200,
            values=["Human", "Bot"],
            command=self.SwitchToAIMode,
        )
        self.OpponentMode.grid(row=3, column=0, pady=50)
        self.AppeareceModeDropDown = ctk.CTkOptionMenu(
            self,
            height=40,
            width=200,
            values=["System", "Light", "Dark"],
            command=self.ChangeAppearanceMode,
        )
        self.AppeareceModeDropDown.grid(row=5, column=0, pady=(10, 50))
        self.ScalingLabel = ctk.CTkLabel(
            self, font=ctk.CTkFont(size=20), text=" Scaling", anchor="center"
        )
        self.ScalingLabel.grid(row=6, column=0, pady=10)
        self.ScalingMenu = ctk.CTkOptionMenu(
            self,
            width=200,
            height=40,
            values=["75%", "80%", "90%", "100%", "110%", "120%", "125%"],
            command=self.ChangeScaling,
        )
        self.ScalingMenu.grid(row=7, column=0, pady=(10, 50))
        self.ScalingMenu.set("100%")
        self.PreferencesButton = ctk.CTkButton(
            self,
            text="Preferences",
            command=self.showPreferences,
            height=30,
            anchor="center",
            image=ctk.CTkImage(
                light_image=Image.open(
                    "chess-2.0\\GUI\\Resources\\Misc\\PreferencesIcon.png"
                ),
                dark_image=Image.open(
                    "chess-2.0\\GUI\\Resources\\Misc\\PreferencesIcon.png"
                ),
                size=(30, 30),
            ),
            compound="left",
        )
        self.PreferencesButton.grid(row=8, column=0, ipadx=10, ipady=10, pady=20)
        self.FenEntry = ctk.CTkEntry(self, textvariable=self.Fen, width=200)
        self.FenEntry.place(x=30, y=250)

    def showPreferences(self):
        Preferences(self.ParentObject).show()

    def CopyFENToClipboard(self):
        BitBoards, BoardData = (
            self.ParentObject.ChessBoardObj.bitboards,
            self.ParentObject.ChessBoardObj.board_data,
        )
        fen = convert_bitboards_to_fen(BitBoards, BoardData)
        import pygame
        import pyperclip

        pygame.image.save(self.ParentObject.Display, "board.png")
        pyperclip.copy(fen)
        messagebox.showinfo(
            "FEN Copied", "The FEN Notation has been added to your Clip Board"
        )

    def ChangeScaling(self, ScalingValue):
        ctk.set_widget_scaling(int(ScalingValue.replace("%", "")) / 100)

    def ChangeAppearanceMode(self, AppearanceMode):
        ctk.set_appearance_mode(AppearanceMode)
        ctk.AppearanceModeTracker.update()
        self.ParentObject.BaseColour = (
            (26, 26, 26)
            if ctk.get_appearance_mode() == "Dark"
            else (242, 242, 242)
        )

    def StartNewGame(self):
        if self.Fen.get():
            BitBoards, BoardData = generate_bitboards_from_board(self.Fen.get())
            self.ParentObject.ChessBoardObj = brains.Board(BitBoards, BoardData)
            self.ParentObject.BitBoards = (
                self.ParentObject.ChessBoardObj.bitboards
            )
            self.ParentObject.BoardData = (
                self.ParentObject.ChessBoardObj.board_data
            )
            self.ParentObject.ValidMoves = (
                self.ParentObject.ChessBoardObj.ReturnMoves()
            )
            self.ParentObject.Turn = self.Fen.get().split()[1].upper()
            self.ParentObject.History = [self.Fen.get()]
            self.Fen.set("")
        else:
            self.ParentObject.Turn = "W"
            BitBoards, BoardData = generate_bitboards_from_board(fenString)
            self.ParentObject.ChessBoardObj = brains.Board(BitBoards, BoardData)
            self.ParentObject.BitBoards = (
                self.ParentObject.ChessBoardObj.bitboards
            )
            self.ParentObject.BoardData = (
                self.ParentObject.ChessBoardObj.board_data
            )
            self.ParentObject.ValidMoves = (
                self.ParentObject.ChessBoardObj.ReturnMoves()
            )
            self.ParentObject.History = [fenString]
            self.ParentObject.CurrentSquare = None
        for label in self.ParentObject.MoveHistory.label_list:
            label.destroy()

    def SwitchToAIMode(self, Mode):
        if Mode == "Bot":
            self.ParentObject.AgainstAI = True
        else:
            self.ParentObject.AgainstAI = False
        self.ParentObject.CurrentSquare = None
