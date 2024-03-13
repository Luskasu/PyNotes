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
        self.tabs = list()
        self.currentTab = 0

        #UPPER BAR
        self.upperBar = customtkinter.CTkFrame(
            root, 
            width = 35, 
            height = 35, 
            fg_color='#FFF2AB', 
            corner_radius=0)
        self.upperBar.pack(anchor='n', fill = 'x')


        
        #BOTTOM BAR
        self.bottomBar = customtkinter.CTkFrame(
            root, 
            width = 35, 
            height = 35, 
            fg_color='#FFF2AB', 
            corner_radius=0)
        self.bottomBar.pack(anchor='s', fill = 'x', side = 'bottom')

        #ADD
        addButton = customtkinter.CTkButton(
            self.upperBar, 
            width = 35, 
            height = 35, 
            fg_color='#FFF2AB', 
            text_color='black', 
            text='+', 
            font = ('verdana', 21), 
            hover_color='#EEE2A0', 
            corner_radius=16, 
            command=self.NewTab)
        addButton.pack(anchor ='nw', side = 'left')

        #SAVE
        saveButton = customtkinter.CTkButton(
            self.upperBar, 
            width = 35, 
            height = 35, 
            fg_color='#FFF2AB', 
            text_color='black', 
            text='Save Note', 
            font = ('verdana', 16), 
            hover_color='#EEE2A0', 
            corner_radius=16, 
            command=self.save)
        saveButton.pack(anchor ='nw', side = 'left')

        #main screen
        self.mainScreen = customtkinter.CTkFrame(
            root, 
            width=600, 
            height=400, 
            fg_color='#FFF7D1', 
            corner_radius=0)
        self.mainScreen.pack(anchor = 'n', fill = 'both', expand = True)
        self.ShowEntries('entries\\')
        root.mainloop()


    def ShowEntries(self, path:str):
        self.selectionScreen = customtkinter.CTkFrame(
            self.mainScreen,
            width=600, 
            height=400, 
            fg_color='#FFF7D1', 
            corner_radius=0)
        self.selectionScreen.pack(anchor = 'n', fill = 'both', expand = True)
        entries = list()

        for i, entry in enumerate(listdir(path)):
            entries.append(customtkinter.CTkButton(
                self.selectionScreen, 
                height = 60, 
                fg_color='#FFF7D1', 
                text_color= 'black', 
                text=entry, 
                font = ('verdana', 12), 
                hover_color='#F2EAC4', 
                corner_radius=0, 
                command = lambda a = entry: self.NewTab(str(a))))
            entries[i].pack(anchor='w', fill = 'x')
    

    def NewTab(self, file:any = None):
        
        #destroy the selection screen
        self.selectionScreen.destroy()

        #create a tab instance
        self.tabs.append(Tab(self.mainScreen, self.bottomBar, file))
        print(f'DEBUG: criada tab {len(self.tabs)}')
        self.currentTab = len(self.tabs) - 1

    def save(self):
        print("DEBUG save chamado")
        self.tabs[self.currentTab].SaveCurrentTab()



class Tab:
    def __init__(self, main:any, bar:any, stuff:any = None):
        tabID = int()
        self.tabName = 'unnamed.txt'
        self.textBox = customtkinter.CTkTextbox(
            main, 
            width=600, 
            height=400, 
            fg_color='#FFF7D1', 
            text_color= 'black', 
            corner_radius=0)
        self.textBox.pack(anchor = 'n', fill = 'both', expand = True)
        if stuff is not None:
            #insert file's stuff to textbox
            text = open('entries\\' + str(stuff), encoding= 'utf-8').read()
            self.textBox.insert("0.0", text)
            self.tabName = str(stuff)
        
        #tab frame
        self.TabFrame = customtkinter.CTkFrame(
            bar,
            width = 70,
            height = 35,
            fg_color='#FFF2AB',
            corner_radius=6)
        self.TabFrame.pack(anchor ='nw', side = 'left', padx = 8)

        #tab title bar
        self.tabTitleBar = customtkinter.CTkButton(
            self.TabFrame,
            width = 70,
            height = 35,
            fg_color='#FFF2AB',
            text_color='black',
            text=self.tabName,
            font = ('verdana', 16),
            hover=False,
            corner_radius=0)
        self.tabTitleBar.pack(anchor ='nw', side = 'left', padx = 4)

        #close button to any bar
        self.closeButton = customtkinter.CTkButton(
            self.TabFrame,
            width = 24,
            height = 30,
            fg_color='#FFF2AB',
            text_color='black',
            text= 'x',
            font = ('verdana', 14, 'bold'),
            hover_color='#EEE2A0',
            corner_radius=32,
            command=self.CloseCurrentTab)
        self.closeButton.pack(anchor ='w', side = 'left')
    
    def SaveCurrentTab(self):
        print("DEBUG SaveCurrentTab")
        fileToSave = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[('text files', '.txt')])
        
        text = str(self.textBox.get(1.0, 'end'))
        fileToSave.write(text)
        fileToSave.close()

    def CloseCurrentTab(self):
        self.textBox.destroy()
        self.TabFrame.destroy()
        
        

w = Window()

