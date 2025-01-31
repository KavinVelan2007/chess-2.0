import customtkinter as ctk
import sqlite3

class Preferences(ctk.CTkToplevel):

    def __init__(self, ParentObject, **kwargs):

        super().__init__()

        self.ParentObject = ParentObject

        self.Piece = ctk.StringVar(value=self.ParentObject.PiecePreference)
        
        self.Board = ctk.StringVar(value=self.ParentObject.BoardPreference)

    def show(self):

        self.geometry('900x700')

        self.PieceDropdown = ctk.CTkOptionMenu(self, variable=self.Piece, values = self.ParentObject.PieceOptions,width=300)
        self.PieceDropdown.place(relx=0.111,rely=0.0142)

        self.BoardDropdown = ctk.CTkOptionMenu(self, variable=self.Board, values = self.ParentObject.BoardOptions,width=300)
        self.BoardDropdown.place(relx=0.555,rely=0.0142)

        self.ApplyButton = ctk.CTkButton(self, command=self.applyPreference, text='Apply')
        self.ApplyButton.place(relx=0.388,rely=0.857)

        self.mainloop()

    def applyPreference(self):

        self.ParentObject.BoardPreference = self.Board.get()

        self.ParentObject.PiecePreference = self.Piece.get()

        sqliteobj = sqlite3.connect('chess-2.0/database.db')

        pyobj = sqliteobj.cursor()

        pyobj.execute('update chess set piece = ?, board = ? where username = ?',(self.Piece.get(),self.Board.get(),self.ParentObject.UserName))

        sqliteobj.commit()

        self.destroy()