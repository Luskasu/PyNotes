import customtkinter
from tkinter import filedialog
from os import listdir, path



class Window:
    lightMode = {
    "bar":"#FFF2AB", 
    "bar_hover":"#EEE2A0", 
    "light":"#FFF7D1", 
    "light_hover":"#F2EAC4", 
    "bg":"#F2ECCC",
    "txt":"#F7F0C9"}

    def __init__(self, width:int = 600, height:int = 400, mode:dict = lightMode):
        self.mode = mode
        customtkinter.set_appearance_mode('dark')
        root = customtkinter.CTk(self.mode["bar"])
        root.geometry(str(width) + 'x' + str(height))
        root.title('PyNotes')
        root.iconbitmap('Assets\\Icon.ico')   
        root.resizable(True, True)
        self.tabs = dict()
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
            command=self.SaveTab)
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

    def ShowEntries(self, folder:str):
        entries = list()
        if path.isdir(folder):
            for i, entry in enumerate(listdir(folder)):
                entries.append(customtkinter.CTkButton(
                    self.selectionScreen, 
                    height = 30, 
                    fg_color= self.mode["light"], 
                    text_color= 'black',
                    text=entry,
                    font = ('verdana', 12), 
                    hover_color=self.mode["light_hover"], 
                    corner_radius=0, 
                    command = lambda a = entry: self.OpenTab(a)))
                entries[i].pack(anchor='w', fill = 'x')
    
    def NewTab(self):
        print('DEBUG: New Tab Chamada')
        #naming a new file
        frame = customtkinter.CTkFrame(
            self.selectionScreen,
            height = 30, 
            fg_color= self.mode["light"])
        frame.place(x=0, y=0)
        name = customtkinter.CTkTextbox(
            frame,
            height = 20,
            fg_color= self.mode["bg"],
            text_color='black',
            font = ('verdana', 12))
        name.pack()


    def OpenTab(self, file:str = None):
        print('DEBUG: OPENTAB' + file)
        #Null verification
        if file is None:
            return
        #verify if tab at less exists
        if len(self.tabs) != 0:
            #verify if tab alread is opened
            for key in self.tabs:
                if key == file:
                    print('DEBUG: você já abriu esse arquivo')
                    return 
        #create a tab instance
        self.tabs.update({file:Tab(self, file)})
        self.SwapTab(self.tabs[file], event='yes')

    
    #this function will load and reload the tabs content
    def SwapTab(self, tab:any, event = None):
        print('DEBUG: SwapTab')
        if self.currentTab is not None:
            self.currentTab.textBox.pack_forget()
            tab.tabFrame.configure(fg_color= self.mode["bar"])
            tab.tabTitleBar.configure(fg_color= self.mode["bar"])
            tab.closeButton.configure(fg_color= self.mode["bar"], hover_color= self.mode["bar_hover"])
        if event is not None:
            tab.tabFrame.configure(fg_color= self.mode["bar_hover"])
            tab.tabTitleBar.configure(fg_color= self.mode["bar_hover"])
            tab.closeButton.configure(fg_color= self.mode["bar_hover"], hover_color= self.mode["light"])
        tab.textBox.pack(anchor = 'n', fill = 'both', expand = True)
        self.currentTab = tab

    def SaveTab(self):
        print("DEBUG save chamado")
        self.currentTab.SaveCurrentTab()



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
            command = lambda event: self.window.SwapTab(self, event))

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
            command = lambda event: self.window.SwapTab(self, event))

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
            command=self.CloseTab)
        self.closeButton.pack(anchor ='w', side = 'left')

    def SaveCurrentTab(self):
        print("DEBUG SaveCurrentTab")
        fileToSave = filedialog.asksaveasfile(
            defaultextension='.txt', 
            filetypes=[('text files', '.txt')])
        
        text = str(self.textBox.get(1.0, 'end'))
        fileToSave.write(text)
        fileToSave.close()

    def CloseTab(self):
        if self is not self.window.currentTab and self.window.currentTab is not None:
            self.textBox.pack(anchor = 'n', fill = 'both', expand = True)
        else:
            #define a new current tab
            self.window.currentTab = self.window.tabs[next(iter(self.window.tabs))]
            self.window.SwapTab(self.window.currentTab)
            
        self.textBox.destroy()
        self.tabFrame.destroy()

        del(self.window.tabs[self.tabName])

w = Window()


#ERROS POR RESOLVER
#1- o save não tá usando o encoding= 'utf-8'. recomendo refazer a função de save
#2 o botão add não funciona
#3 o menu de arquivos é feio. fazer um menu que acesse várias pastas (com subdiretórios) e com menu de contexto (como o do vs code) que permita renomear os arquivos ou ewxcluir eles)