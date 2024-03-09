import customtkinter
from tkinter import filedialog
from os import listdir

class Window:
    def __init__(self):
        customtkinter.set_appearance_mode('dark')
        root = customtkinter.CTk('#FFF2AB')
        root.geometry("600x400+200+200")
        root.title('PyNotes')
        root.iconbitmap('Assets\\Icon.ico')   
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        #UPPER BAR
        self.upperBar = customtkinter.CTkFrame(root, width = 35, height = 35, fg_color='#FFF2AB', corner_radius=0)
        self.upperBar.pack(anchor='n', fill = 'x')
        
        #BOTTOM BAR
        bottomBar = customtkinter.CTkFrame(root, width = 35, height = 35, fg_color='#FFF2AB', corner_radius=0)
        bottomBar.pack(anchor='s', fill = 'x', side = 'bottom')

        #ADD
        AddButton = customtkinter.CTkButton(self.upperBar, width = 35, height = 35, fg_color='#FFF2AB', text_color='black', text='+', font = ('verdana', 21), hover_color='#EEE2A0', corner_radius=0)
        AddButton.pack(anchor ='nw', side = 'left')

        #main screen
        self.screen = customtkinter.CTkFrame(root, width=600, height=400, fg_color='#FFF7D1', corner_radius=0)
        self.screen.pack(anchor = 'n', fill = 'both', expand = True)
        

        self.ShowEntries('entries\\')
        root.mainloop()
        
        
    def ShowEntries(self, path:str):
        self.selection = customtkinter.CTkFrame(self.screen, width=600, height=400, fg_color='#FFF7D1', corner_radius=0)
        self.selection.pack(anchor = 'n', fill = 'both', expand = True)
        entries = list()
        for i, entry in enumerate(listdir(path)):
            entries.append(customtkinter.CTkButton(self.selection, height = 60, fg_color='#FFF7D1', text_color= 'black', text=entry, font = ('verdana', 12), hover_color='#F2EAC4', corner_radius=0, command = lambda a = entry: self.OpenEntry('entries\\'+a)))
            entries[i].pack(anchor='w', fill = 'x')
        
    
    def OpenEntry(self, fileToOpen):
        print('opening the file at:  ' + fileToOpen)

        #destroy the selection screen
        self.selection.destroy()

        #create a the textbox screen
        textBox = customtkinter.CTkTextbox(self.screen,width=600, height=400, fg_color='#FFF7D1', text_color= 'black', corner_radius=0)
        textBox.pack(anchor = 'n', fill = 'both', expand = True)

        text = open(fileToOpen).read()
        textBox.insert("0.0", text)
        

w = Window()