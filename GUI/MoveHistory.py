import customtkinter

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")

        self.label_list = []

        self.column = 0

        self.row = 0


    def add_item(self, item):
        
        label = customtkinter.CTkLabel(self, text_color='white', text=item, font=customtkinter.CTkFont(size=25),padx=5,pady=5)

        label.grid(row=self.row, column=self.column, padx=2, pady=5)

        self.label_list += [label]

        self.column += 1

        if self.column == 2:

            self.row += 1
            
            self.column = 0