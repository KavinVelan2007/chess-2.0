import customtkinter as ctk
from GUIGameFrame import GameFrame


def global_init():
    ctk.deactivate_automatic_dpi_awareness()


class App(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry(self.CenterWindowToDisplay(1280, 720))
        self._set_appearance_mode('dark')
        self.configure(fg_color = ('#D8D8D8', '#303030'))
        self.title('Chess')
        self.resizable(False, False)

        self.game_running = False
        
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius = 20, width = 225, height = 720, fg_color = ('#F0F0F0', '#101010'), bg_color = ('#D8D8D8', '#303030'))
        self.sidebar_frame._set_appearance_mode(self._get_appearance_mode())
        self.sidebar_frame.place(x = 0, y = 0, anchor = 'nw')
        self.sidebar_frame.grid_propagate(False)
        
        self.sidebar_frame.grid_columnconfigure(0, weight = 1)
        self.sidebar_frame.grid_rowconfigure((3, ), weight = 1)
        self.sidebar_frame.grid_rowconfigure((0, 1, 2, 4), weight = 0)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text = "Options", font = ctk.CTkFont(size = 25, weight="bold", family = "Cascadia Code SemiBold"))
        self.logo_label._set_appearance_mode(self._get_appearance_mode())
        self.logo_label.grid(row = 0, column = 0, pady = 30)
        
        self.new_game_ai = ctk.CTkButton(self.sidebar_frame, text = "New Game with AI", command = self.on_ai_button, font = ctk.CTkFont(size = 17, weight="normal", family = "Cascadia Code SemiBold"), fg_color = ('blue', 'darkblue'))
        self.new_game_ai.grid(row = 1, column = 0, pady = 20, ipadx = 10, ipady = 15)
        self.new_game_ai._set_appearance_mode(self._get_appearance_mode())

        self.new_game_person = ctk.CTkButton(self.sidebar_frame, text = "New Game with\na Friend", command = self.on_person_button, font = ctk.CTkFont(size = 17, weight="normal", family = "Cascadia Code SemiBold"), fg_color = ('blue', 'darkblue'))
        self.new_game_person.grid(row = 2, column = 0, pady = 20, ipadx = 10, ipady = 15)
        self.new_game_person._set_appearance_mode(self._get_appearance_mode())

        self.preferences_button = ctk.CTkButton(self.sidebar_frame, text = "Preferences", font = ctk.CTkFont(size = 25, weight="normal", family = "Cascadia Code SemiBold"), fg_color = ('blue', 'darkblue'))
        self.preferences_button._set_appearance_mode(self._get_appearance_mode())
        self.preferences_button.grid(row = 3, column = 0, pady = 20, ipadx = 10, ipady = 15, sticky = 's')

        self.quit_button = ctk.CTkButton(self.sidebar_frame, text = "Quit", command = self.on_quit, font = ctk.CTkFont(size = 25, weight="normal", family = "Cascadia Code SemiBold"), fg_color = ('red', 'darkred'))
        self.quit_button._set_appearance_mode(self._get_appearance_mode())
        self.quit_button.grid(row = 4, column = 0, pady = 20, ipadx = 10, ipady = 15, sticky = 's')

        self.gameframe = GameFrame(self)
        self.gameframe.place(x = 275, y = 50, anchor = 'nw')
        self.gameframe.grid_propagate(False)


        self.mainloop()
    

    def CenterWindowToDisplay(self, width, height):
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2) - 50)
        return f"{width}x{height}+{x}+{y}"


    def on_quit(self):
        self.destroy()


    def on_ai_button(self):
        pass


    def on_person_button(self):
        pass



class ToplevelWindow(ctk.CTkToplevel):

    def __init__(self):

        super().__init__()
        self.geometry("400x300")


global_init()
a = App()