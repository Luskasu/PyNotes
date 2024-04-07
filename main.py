import customtkinter
from os import listdir, path, remove, rename
from constants import *
from tkinter import Menu
from PIL import Image

class Window(customtkinter.CTk):
    def __init__(self, width:int = 900, height:int = 600, mode:dict = LIGHT_MODE):
        
        self.mode = mode
        customtkinter.set_appearance_mode('dark')
        super().__init__(self.mode["bar"])
        self.geometry(str(width) + 'x' + str(height))
        self.title('PyNotes')
        self.iconbitmap('Assets\\Icon.ico')
        self.resizable(True, True)
        self.tabs = list()
        self.currentTab = None
        self.entries = list()

        #UPPER BAR
        self.toolBar = customtkinter.CTkFrame(
            self,
            fg_color=self.mode["bar"], 
            corner_radius=0)
        self.toolBar.pack(side = 'top', fill = 'x')

        #ADD
        addButton = Button(self.toolBar, self.mode, '+', self.newFileField, ('verdana', 18, 'bold'))
        saveButton = Button(self.toolBar, self.mode, 'Save Note', lambda: self.saveTab(self.currentTab))

        self.selectionScreen = customtkinter.CTkFrame(
            self,
            fg_color=self.mode["light"], 
            corner_radius=0)
        self.selectionScreen.pack_propagate(0)
        self.selectionScreen.pack(side = 'left', fill = 'y')
        
        self.explorerLabel = customtkinter.CTkLabel(
            self.selectionScreen,
            height = 32,
            text= 'EXPLORER',
            text_color='black',
            font=('verdana', 12),
            fg_color=self.mode["light"],
            corner_radius=0
        )
        self.explorerLabel.pack(anchor = 'w', padx = 18)
        
        self.pathLabel = customtkinter.CTkLabel(
            self.selectionScreen,
            height=0,
            text= FOLDER,
            text_color='black',
            font=('verdana', 10),
            fg_color=self.mode["light"],
            corner_radius=0
        )
        self.pathLabel.pack(anchor = 'w', padx = 18)
        
        #main screen
        self.mainScreen = customtkinter.CTkFrame(
            self, 
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
        
        self.showEntries()        
        self.mainloop()
    
    def showEntries(self):
        if not path.isdir(FOLDER):
            return
        if len(self.entries) > 0:
            for entry in self.entries:
                entry.destroy()
            self.entries.clear()
        
        for entry in listdir(FOLDER):
            self.entries.append(File(self.selectionScreen, entry, self))

    def newFileField(self):
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
        self.showEntries()   

    def newFile(self):
        filepath = str(self.title.get(1.0, 'end')).strip()
        if not filepath.endswith('.txt') or not filepath.endswith('.py'):
            filepath = filepath + '.txt'
        file = open(FOLDER + filepath, 'w')
        file.write('')
        file.close()
        self.showEntries()
        self.frame.destroy()

    def OpenTab(self, file:str):
        if self.currentTab is not None:
            for tab in self.tabs:
                if tab.tabName == file:
                    self.swapTab(tab)
                    return
        self.tabs.append(Tab(self, file))
        self.swapTab(self.tabs[-1])
    
    def swapTab(self, tab:any, event = None):
        if self.currentTab is not None:
            self.currentTab.textBox.pack_forget()
            self.currentTab.turnUnhover()
        tab.textBox.pack(anchor = 'n', fill = 'both', expand = True)
        tab.turnHover()
        
        self.currentTab = tab

    def saveTab(self, tab:any):
        with open(FOLDER+tab.tabName, 'w', encoding='utf-8') as file:
            file.write(tab.getContent())
            

class Tab:
    def __init__(self, window, file:str = None):
        self.tabName = file
        self.window = window
        self.textBox = customtkinter.CTkTextbox(
            self.window.mainScreen,
            width= 600,
            height= 400,
            fg_color=window.mode["txt_box"], 
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
            command = lambda event: self.window.swapTab(self, event))

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
            command = lambda event: self.window.swapTab(self, event))

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
        
        actual = self.window.tabs.index(self.window.currentTab)
        if actual == len(self.window.tabs) - 1:
            actual = -1
        self.window.tabs.remove(self)
        
        if len(self.window.tabs) == 0:
            self.window.currentTab = None
            return
        self.window.currentTab = self.window.tabs[int(actual)]
        self.window.swapTab(self.window.currentTab)


class Button(customtkinter.CTkButton):
    def __init__(self, parent:any, mode:dict, stuff:str, func, font = ('verdana', 14)):
        self.mode = mode
        if path.isfile(stuff):
            self.text = None
            self.image = customtkinter.CTkImage(Image.open(stuff), size=(30,30))
        else:
            self.text = stuff
            self.image = None
            
        super().__init__(
            parent, 
            35, 35, 16,
            text = self.text,
            image= self.image,
            fg_color=self.mode["bar"],
            text_color='black',
            hover_color=self.mode["bar_hover"],
            font = font,
            command = func)
        self.pack(side = 'left')


class File(customtkinter.CTkButton):
    def __init__(self, parent, entry:str, window):
        self.fileName = entry
        self.window = window
        super().__init__(
            parent, 
            height = 30, 
            fg_color= self.window.mode["light"], 
            text_color= 'black',
            text=entry,
            font = ('verdana', 12), 
            hover_color=self.window.mode["light_hover"], 
            corner_radius=0, 
            command = lambda: self.window.OpenTab(entry)
        )
        self.pack(anchor='w', fill = 'x')
            
    
        #Context Menu
        self.context_menu = Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Rename", command = self.renameField)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command = self.deleteFile)
        self.bind("<Button-3>", self.showMenu)

    def showMenu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
    
    def renameField(self):
        self.frame = customtkinter.CTkFrame(
            self.window.selectionScreen,
            height = 30, 
            fg_color= self.window.mode["light"])
        self.frame.pack()
        self.title = customtkinter.CTkTextbox(
            self.frame,
            height = 20,
            fg_color= self.window.mode["bg"],
            text_color='black',
            font = ('verdana', 12))
        self.title.pack() 
        self.title.bind('<Return>', lambda a: self.renameFile())  
        
    def renameFile(self):
        newName = FOLDER + str(self.title.get(1.0, 'end')).strip()
        oldName = FOLDER + self.fileName
        if not newName.endswith('.txt') or not newName.endswith('.py'):
            newName = newName + '.txt'
        rename(oldName, newName)
        
        self.window.showEntries()
        self.frame.destroy()
    
    def deleteFile(self):
        remove(FOLDER + self.fileName)
        for tab in self.window.tabs:
            if tab.tabName == self.fileName:
                tab.closeTab()
        self.window.showEntries()

if __name__ == '__main__':
    w = Window()
