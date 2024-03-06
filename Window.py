import customtkinter

class Window:
    def __init__(self) -> None:
        customtkinter.set_appearance_mode('dark')
        self.root = customtkinter.CTk('#FFF2AB')
        self.root.geometry("600x400")
        self.root.title('PyNotes')
        self.root.iconbitmap('Assets\\Icon.ico')        

        #buttons
        button = customtkinter.CTkButton(self.root, width=50, height=50, text='+')
        button.pack(anchor ='nw')

        #creating the entry
        entry = customtkinter.CTkTextbox(self.root, width=600, height=400, fg_color='#FFF2AB', text_color= 'black')
        entry.pack(anchor = 'n', fill = 'both', expand = True)

        

        
        


        self.root.mainloop()
        

w = Window()