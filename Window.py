import customtkinter
from os import listdir, path

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
        self.selection = customtkinter.CTkFrame(root, width=600, height=400, fg_color='#FFF7D1', corner_radius=0)
        self.selection.pack(anchor = 'n', fill = 'both', expand = True)

        self.showEntries('entries\\')
        root.mainloop()
        
        
    def showEntries(self, path:str):
        entries = list()
        for i, entry in enumerate(listdir(path)):
            entries.append(customtkinter.CTkButton(self.selection, height = 60, fg_color='#FFF7D1', text_color= 'black', text=entry,font = ('verdana', 12), hover_color='#F2EAC4', corner_radius=0))
            #entries[i] = customtkinter.CTkButton(self.selection,width = 50, height = 50, fg_color='white', text=entry)
            entries[i].pack(anchor='w', fill = 'x')
            
        

w = Window()