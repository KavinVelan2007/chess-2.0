import customtkinter as ctk

from GUI.SideBar import SideBar

ctk.set_default_color_theme("GUI\\Themes.json")


class Game(ctk.CTk):


    def __init__(self, BitBoards, BoardData):

        super().__init__()

        self.minsize(1280, 720)

        # ctk.set_appearance_mode('light')

        self.title('Chess')

        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(0, weight=1)

        self.SideBarFrame = SideBar(self)

        self.mainloop()
