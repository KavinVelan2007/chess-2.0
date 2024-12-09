import customtkinter

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master):
        super().__init__(master, height=700, width=300)

        self.label_list = []

        self.column = 0

        self.row = 0


    def add_item(self, item):
        
        label = customtkinter.CTkLabel(self, text_color='black', text=item, font=customtkinter.CTkFont(size=15), fg_color="#808080",padx=10,pady=10)

        label.grid(row=self.row, column=self.column, padx=5, pady=10)

        self.label_list += [label]

        self.column += 1

        if self.column == 6:

            self.row += 1
            
            self.column = 0