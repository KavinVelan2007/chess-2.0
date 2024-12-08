import customtkinter as ctk
import os
import subprocess

CWD = os.getcwd()

class Main(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.Choice = ctk.StringVar()

        self.DropDown = ctk.CTkComboBox(self, values=['Chess 2.0','Photo Editor','Music Player'], variable=self.Choice)

        self.DropDown.pack(padx=150,pady=150)

        self.StartButton = ctk.CTkButton(self, text='Start', command=self.StartApp)

        self.StartButton.pack(padx=150,pady=10)

        self.mainloop()

    def StartApp(self):

        if self.Choice.get() == 'Chess 2.0':

            subprocess.call(['python','chess-2.0/run.py'])

        elif self.Choice.get() == 'Photo Editor':

            subprocess.call(['python', 'Final-Project-Photo-Editor-/run.py'])

        elif self.Choice.get() == 'Music Player':

            subprocess.call(['python', 'new-not-spotify-/login_page2.py'])

a = Main()