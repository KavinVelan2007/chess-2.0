import customtkinter as ctk

import tkinter

from PIL import Image

ctk.set_default_color_theme("GUI\\Themes.json")


class SideBar(ctk.CTkFrame):


    def __init__(self, Master):

        self.Master = Master

        super().__init__(self.Master)

        self.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure((3, ), weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.LogoLabel = ctk.CTkLabel(
            self, text="Chess", font=ctk.CTkFont(size=25, weight="bold"))

        self.LogoLabel.grid(row=0, column=0, padx=30, pady=20)

        self.NewGameButton = ctk.CTkButton(
            self, text="➕  New Game", height=30, anchor="center")

        self.NewGameButton.grid(row=1, column=0, ipadx=10, ipady=10, pady=20)

        self.SaveQuitButton = ctk.CTkButton(self, height=25, text="Save Progress", image=ctk.CTkImage(light_image=Image.open(
            "GUI\\Resources\\Misc\\SaveIcon.png"), dark_image=Image.open("GUI\\Resources\\Misc\\SaveIcon.png"), size=(25, 25)), anchor="center")

        self.SaveQuitButton.grid(row=2, column=0, ipadx=10, ipady=10, pady=20)

        self.AppeareceModeLabel = ctk.CTkLabel(self, font=ctk.CTkFont(size=20), text=" Appearance Mode", anchor="center", image=ctk.CTkImage(light_image=Image.open(
            "GUI\\Resources\\Misc\\AppearanceModeIcon.png"), dark_image=Image.open("GUI\\Resources\\Misc\\AppearanceModeIcon.png"), size=(30, 30)), compound="left")

        self.AppeareceModeLabel.grid(
            row=4, column=0, ipadx=10, ipady=10, padx=20, pady=10, sticky="s")

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

        self.AccountButton = ctk.CTkButton(self, text="Account", height=30, anchor="center", image=ctk.CTkImage(light_image=Image.open(
            "GUI\\Resources\\Misc\\AccountIcon.png"), dark_image=Image.open("GUI\\Resources\\Misc\\AccountIcon.png"), size=(30, 30)), compound="left")

        self.AccountButton.grid(
                row=8, column=0, ipadx=10, ipady=10, pady=20)


        """
        self.PlayFriendLocal = ctk.CTkButton(
            self, text = "🤝♟ Friend (Local)", anchor = "center")

        self.PlayFriendLocal.grid(row=2, column=0, ipadx = 10, ipady = 15)

        self.PlayFriendOnline = ctk.CTkButton(
            self, text = "Play with a Friend (Online)", width = 240, anchor = "w")

        self.PlayFriendOnline.grid(row=3, column=0, ipadx = 10, ipady = 15)
        """
        """
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(
            self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"])
        """


    def ChangeScaling(self, ScalingValue):

        ctk.set_widget_scaling(
        int(ScalingValue.replace('%', '')) / 100)


    def ChangeAppearanceMode(self, AppearanceMode):

        ctk.set_appearance_mode(AppearanceMode)
