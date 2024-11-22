import customtkinter as ctk
from GUI.SideBar import SideBar

ctk.set_default_color_theme("GUI\\Themes.json")

class TabView(ctk.CTkTabview):

    def __init__(self, window,**kwargs):

        super().__init__(window,**kwargs)

        self.add('Sign In')

        self.add('Sign Up')

class Account(ctk.CTk):
    
    def __init__(self):

        super().__init__()

        self.minsize(1280, 720)

        self.title('Account')

        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(0, weight=1)

        self.tab_view = TabView(self,width=1440,height=820)

        self.tab_view.grid(row=0,column=2)