import customtkinter
from tkinter import filedialog
from os import listdir, path

class Window:
    FOLDER = 'entries\\'

    lightMode = {
    "bar":"#FFF2AB", 
    "bar_hover":"#EEE2A0", 
    "light":"#FFF7D1", 
    "light_hover":"#F2EAC4",
    "selected": "gray",
    "bg":"#F2ECCC",
    "txt":"#F7F0C9"}

    def __init__(self, width:int = 900, height:int = 600, mode:dict = lightMode):
        self.mode = mode
        customtkinter.set_appearance_mode('dark')
        root = customtkinter.CTk(self.mode["bar"])
        root.geometry(str(width) + 'x' + str(height))
        root.title('PyNotes')
        root.iconbitmap('Assets\\Icon.ico')
        root.resizable(True, True)
        self.tabs = list()
        self.currentTab = None
        self.entries = list()

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
            command=self.NewFileField)
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
            command= lambda: self.SaveTab(self.currentTab))
        saveButton.pack(side = 'left')

        self.selectionScreen = customtkinter.CTkFrame(
            root,
            fg_color=self.mode["light"], 
            corner_radius=0)
        self.selectionScreen.pack_propagate(0)
        self.selectionScreen.pack(side = 'left', fill = 'y')
        
        self.explorerLabel = customtkinter.CTkLabel(
            self.selectionScreen,
            text= 'EXPLORER',
            text_color='black',
            font=('verdana', 12),
            fg_color=self.mode["light"],
            corner_radius=0
        )
        self.explorerLabel.pack(anchor = 'w', padx = 18)
        
        self.ShowEntries()
        
        
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

    def ShowEntries(self):
        if not path.isdir(self.FOLDER):
            return
        if len(self.entries) != 0:
            for entry in self.entries:
                entry.destroy()
            self.entries.clear()

        for i, entry in enumerate(listdir(self.FOLDER)):
            self.entries.append(customtkinter.CTkButton(
                self.selectionScreen, 
                height = 30, 
                fg_color= self.mode["light"], 
                text_color= 'black',
                text=entry,
                font = ('verdana', 12), 
                hover_color=self.mode["light_hover"], 
                corner_radius=0, 
                command = lambda a = entry: self.OpenTab(a)))
            self.entries[i].pack(anchor='w', fill = 'x')
    
    def NewFileField(self):
        self.frame = customtkinter.CTkFrame(
            self.selectionScreen,
            height = 30, 
            fg_color= self.mode["light"])
        self.frame.pack()
        self.title = customtkinter.CTkTextbox(
            self.frame,
            height = 20,
            fg_color= self.mode["bg"],
            text_color='black',
            font = ('verdana', 12))
        self.title.pack() 
        self.title.bind('<Return>', lambda e: self.newFile())
        self.ShowEntries()
        

    def newFile(self):
        filepath = str(self.title.get(1.0, 'end')).strip()
        if not filepath.endswith('.txt') or not filepath.endswith('.py'):
            filepath = filepath + '.txt'
        file = open(self.FOLDER + filepath, 'w')
        file.write('')
        file.close()
        self.ShowEntries()

        self.frame.destroy()

    def OpenTab(self, file:str):
        if self.currentTab is not None:
            for tab in self.tabs:
                if tab.tabName == file:
                    print('DEBUG: você já abriu o arquivo' + file)
                    return

        self.tabs.append(Tab(self, file))
        self.swapTab(self.tabs[-1])

    def swapTab(self, tab:any):
        if self.currentTab is not None:
            self.currentTab.textBox.pack_forget()
            self.currentTab.turnUnhover()
        tab.textBox.pack(anchor = 'n', fill = 'both', expand = True)
        tab.turnHover()
        
        self.currentTab = tab

    def SaveTab(self, tab:any):
        with open(self.FOLDER+tab.tabName, 'w', encoding='utf-8') as file:
            file.write(tab.getContent())



class Tab():
    def __init__(self, window, file:str = None):
        self.tabName = file
        self.window = window
        self.textBox = customtkinter.CTkTextbox(
            self.window.mainScreen,
            width= 600,
            height= 400,
            fg_color=window.mode["txt"], 
            text_color= 'black', 
            corner_radius=0)

        pathToFile = 'entries\\' + file
        if path.isfile(pathToFile):
            text = open(pathToFile, encoding= 'utf-8').read()
            self.textBox.insert("0.0", text)

        #tab button
        self.tabFrame = customtkinter.CTkFrame(
            self.window.bottomBar,
            width = 90,
            height = 35,
            fg_color= window.mode["bar"],
            corner_radius=6)
        self.tabFrame.pack(anchor ='nw', side = 'left')
        self.tabFrame.bind(
            "<Button-1>", 
            command = lambda event: self.window.swapTab(self))

        #tab title
        self.tabTitleBar = customtkinter.CTkLabel(
            self.tabFrame,
            width = 90,
            height = 35,
            fg_color='#FFF2AB',
            text_color='black',
            text=self.tabName,
            font = ('verdana', 14),
            corner_radius=0)
        self.tabTitleBar.pack(anchor ='w', side = 'left', padx = 4)
        self.tabTitleBar.bind(
            "<Button-1>", 
            command = lambda event: self.window.swapTab(self))

        #close button to any bar
        self.closeButton = customtkinter.CTkButton(
            self.tabFrame,
            width = 24,
            height = 30,
            fg_color='#FFF2AB',
            text_color='black',
            text= 'x',
            font = ('verdana', 14, 'bold'),
            hover_color= window.mode["bar_hover"],
            corner_radius=32,
            command=self.closeTab)
        self.closeButton.pack(anchor ='w', side = 'left')
        
    def getContent(self) -> str:
        return self.textBox.get(1.0, 'end')
    
    def turnHover(self):
        self.tabFrame.configure(fg_color= self.window.mode["bar_hover"])
        self.tabTitleBar.configure(fg_color= self.window.mode["bar_hover"])
        self.closeButton.configure(
            fg_color= self.window.mode["bar_hover"], 
            hover_color= self.window.mode["light"])
    
    def turnUnhover(self):
        self.tabFrame.configure(fg_color= self.window.mode["bar"])
        self.tabTitleBar.configure(fg_color= self.window.mode["bar"])
        self.closeButton.configure(
            fg_color= self.window.mode["bar"], 
            hover_color= self.window.mode["bar_hover"])

    def closeTab(self):
        if self is self.window.currentTab:
            self.closeCurrent()
            return
        self.textBox.destroy()
        self.tabFrame.destroy()
        self.window.tabs.remove(self)
    
    def closeCurrent(self):
        self.textBox.destroy()
        self.tabFrame.destroy()
        self.window.tabs.remove(self)
        
        if len(self.window.tabs) == 0:
            print('last')
            self.window.currentTab = None
            return
        
        self.window.currentTab = self.window.tabs[-1]
        self.window.swapTab(self.window.currentTab)
        
    
        

w = Window()


#ERROS POR RESOLVER
# 0 SE FECHAR o ultimo da erro
#1- o save não tá usando o encoding= 'utf-8'. recomendo refazer a função de save
#2 o menu de arquivos é feio. fazer um menu que acesse várias pastas (com subdiretórios) e com menu de contexto (como o do vs code) que permita renomear os arquivos ou ewxcluir eles)
#n