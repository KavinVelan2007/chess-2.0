import customtkinter as ctk
import sqlite3
import tkinter.messagebox
from GUI.Defaults import DEFAULT_BOARD_THEME, DEFAULT_PIECE_THEME
from GUI.Main import Game
from GUI.Paths import DATABASE_PATH, FEN_STRING_PATH, THEME_PATH
from GUI.WindowUtils import maximize_window
from fen import *


ctk.set_default_color_theme(THEME_PATH)


class TabView(ctk.CTkTabview):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.add("Sign In")
        self.add("Sign Up")
        self.tab("Sign Up").grid_rowconfigure(1, weight=1)
        self.tab("Sign Up").grid_columnconfigure(1, weight=1)
        self.tab("Sign In").grid_rowconfigure(1, weight=1)
        self.tab("Sign In").grid_columnconfigure(1, weight=1)


class Account(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.sqliteobj = sqlite3.connect(DATABASE_PATH)
        self.pyobj = self.sqliteobj.cursor()
        self.pyobj.execute(
            "create table if not exists chess (username varchar(50), password "
            "varchar(50), piece varchar(30), board varchar(30))"
        )
        self.username = ctk.StringVar()
        self.password = ctk.StringVar()
        self.minsize(1280, 720)
        self.title("Account")
        maximize_window(self)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.tab_view = TabView(self, width=500, height=400)
        self.loadSignUpWidgets()
        self.loadSignInWidgets()
        self.tab_view.grid(row=1, column=1)
        self.mainloop()

    def loadSignUpWidgets(self):
        self.usernameEntry = ctk.CTkEntry(
            self.tab_view.tab("Sign Up"),
            textvariable=self.username,
            width=300,
        )
        self.usernameEntry.grid(row=0, column=1, pady=60)
        self.signUpLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign Up"),
            text="Enter User Name",
            font=("Helvetica", 20),
        )
        self.signUpLabel.place(x=170, y=30)
        self.passwordEntry = ctk.CTkEntry(
            self.tab_view.tab("Sign Up"),
            textvariable=self.password,
            width=300,
            show="*",
        )
        self.passwordEntry.place(x=93, y=180)
        self.passwordLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign Up"),
            text="Enter Password",
            font=("Helvetica", 20),
        )
        self.passwordLabel.place(x=175, y=150)
        self.submit = ctk.CTkButton(
            self.tab_view.tab("Sign Up"),
            text="Submit",
            command=self.createAccount,
        )
        self.submit.place(x=180, y=255)
        self.statusLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign Up"), text="", font=("Helvetica", 30)
        )
        self.statusLabel.grid(row=2, column=1)

    def loadSignInWidgets(self):
        self.usernameEntry = ctk.CTkEntry(
            self.tab_view.tab("Sign In"),
            textvariable=self.username,
            width=300,
        )
        self.usernameEntry.grid(row=0, column=1, pady=60)
        self.signInLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign In"),
            text="Enter User Name",
            font=("Helvetica", 20),
        )
        self.signInLabel.place(x=170, y=30)
        self.passwordEntry = ctk.CTkEntry(
            self.tab_view.tab("Sign In"),
            textvariable=self.password,
            width=300,
            show="*",
        )
        self.passwordEntry.place(x=93, y=180)
        self.passwordLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign In"),
            text="Enter Password",
            font=("Helvetica", 20),
        )
        self.passwordLabel.place(x=175, y=150)
        self.submit = ctk.CTkButton(
            self.tab_view.tab("Sign In"), text="Submit", command=self.signIn
        )
        self.submit.place(x=180, y=255)
        self.statusLabel = ctk.CTkLabel(
            self.tab_view.tab("Sign In"), text="", font=("Helvetica", 30)
        )
        self.statusLabel.grid(row=2, column=1)

    def createAccount(self):
        username = self.username.get()
        password = self.password.get()
        if username and password:
            self.pyobj.execute(
                "select username,password from chess where username = ?",
                (username,),
            )
            if not self.pyobj.fetchall():
                self.pyobj.execute(
                    "insert into chess values (?, ?, ?, ?)",
                    (
                        username,
                        password,
                        DEFAULT_PIECE_THEME,
                        DEFAULT_BOARD_THEME,
                    ),
                )
                self.sqliteobj.commit()
                self.destroy()
                self.startGame(username)
            else:
                tkinter.messagebox.showerror(
                    "User Exists", "A user with the same username exists"
                )
        else:
            tkinter.messagebox.showerror(
                "Field Empty", "All Fields must be filled"
            )

    def signIn(self):
        username = self.username.get()
        password = self.password.get()
        if username and password:
            self.pyobj.execute(
                "select * from chess where username = ? and password = ?",
                (username, password),
            )
            d = self.pyobj.fetchall()
            if d:
                self.destroy()
                self.startGame(username)
            else:
                self.statusLabel.configure(text="Wrong Credentials")

    def startGame(self, username):
        with open(FEN_STRING_PATH, "r"):
            BitBoards, BoardData = generate_bitboards_from_board(fenString)
        MainGame = Game(
            BitBoards=BitBoards, BoardData=BoardData, username=username
        )
