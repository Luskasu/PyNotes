import customtkinter
from tkinter import filedialog
from os import listdir

lightMode = {
    "bar":"#FFF2AB", 
    "bar_hover":"#EEE2A0", 
    "light":"#FFF7D1", 
    "light_hover":"#F2EAC4", 
    "bg":"#F2ECCC"}

class Window:
    def __init__(self, width:int = 600, height:int = 400, mode:dict = lightMode):
        self.mode = mode
        customtkinter.set_appearance_mode('dark')
        root = customtkinter.CTk(self.mode["bar"])
        root.geometry(str(width) + 'x' + str(height))
        root.title('PyNotes')
        root.iconbitmap('Assets\\Icon.ico')   
        root.resizable(True, True)
        self.tabs = list()
        self.currentTab = None

        #UPPER BAR
        self.upperBar = customtkinter.CTkFrame(
            root,
            fg_color=self.mode["bar"], 
            corner_radius=0)
        self.upperBar.pack(side = 'top', fill = 'x')

        #ADD
        addButton = customtkinter.CTkButton(
            self.upperBar, 
            width = 35, 
            height = 35, 
            fg_color=self.mode["bar"], 
            text_color='black', 
            text='+', 
            font = ('verdana', 21), 
            hover_color= self.mode["bar_hover"],
            corner_radius=16, 
            command=self.NewTab)
        addButton.pack(side = 'left')

        #SAVE
        saveButton = customtkinter.CTkButton(
            self.upperBar, 
            width = 35, 
            height = 35, 
            fg_color=self.mode["bar"], 
            text_color='black', 
            text='Save Note', 
            font = ('verdana', 14), 
            hover_color=self.mode["bar_hover"], 
            corner_radius=16, 
            command=self.save)
        saveButton.pack(side = 'left')


        #selection screen
        self.selectionScreen = customtkinter.CTkFrame(
            root,
            fg_color=self.mode["light"], 
            corner_radius=0)
        self.selectionScreen.pack(side = 'left', fill = 'y')
        self.ShowEntries('entries\\')

        #main screen
        self.mainScreen = customtkinter.CTkFrame(
            root, 
            fg_color=mode["bg"],
            corner_radius=0)
        self.mainScreen.pack(side = 'left', fill = 'both', expand = True)

        #BOTTOM BAR
        self.bottomBar = customtkinter.CTkFrame(
            self.mainScreen, 
            height = 35, 
            fg_color=self.mode["bar"], 
            corner_radius=0)
        self.bottomBar.pack(side = 'bottom', fill = 'x')

        root.mainloop()

    def ShowEntries(self, path:str):
        entries = list()

        for i, entry in enumerate(listdir(path)):
            entries.append(customtkinter.CTkButton(
                self.selectionScreen, 
                height = 60, 
                fg_color= self.mode["light"], 
                text_color= 'black',
                text=entry,
                font = ('verdana', 12), 
                hover_color=self.mode["light_hover"], 
                corner_radius=0, 
                command = lambda a = entry: self.NewTab(a)))
            
            entries[i].pack(anchor='w', fill = 'x')
    

    def NewTab(self, file:any = None):
        print(self.tabs)
        #verify if tab at less exists
        if len(self.tabs) == 0:
            print('verificado, é a primeira tab criada')
        else:
            print('já tem tabs criadas')

        #create a tab instance
        self.tabs.append(Tab(self, file))
        
        print(f'DEBUG: criada tab {len(self.tabs)}')

        self.currentTab = len(self.tabs) - 1

    def save(self):
        print("DEBUG save chamado")
        self.tabs[self.currentTab].SaveCurrentTab()



class Tab():
    def __init__(self, window, stuff:any = None):
        self.window = window
        self.textBox = customtkinter.CTkTextbox(
            self.window.mainScreen, 
            width= 600,
            height= 400,
            fg_color=window.mode["light"], 
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
            self.window.bottomBar,
            width = 70,
            height = 35,
            fg_color= window.mode["bar"],
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
            hover_color= window.mode["bar_hover"],
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

#  1) verificar se uma entrada ja foi convertida em tab antes de carregar ela como tab
#  2) pra onde vai o texto?