from tkinter.filedialog import *
import tkinter

def SaveFile():
    fileToSave = asksaveasfile(filetypes=[('.txt', 'txt')])
    if fileToSave is None:
        return
    text = str(entry.get(1.0, 'end'))
    fileToSave.write(text)
    fileToSave.close()


#created an instance and setted some config
canvas = tkinter.Tk()
canvas.geometry('400x600')
canvas.title('PyNotes')
canvas.config(bg = '#E6E2DD')

#seting am frame margin
topFrame = tkinter.Frame(canvas)
topFrame.pack(padx = 10, pady= 5, anchor='nw')

#Some bottons bellow
OpenB = tkinter.Button(canvas, text='Open', bg = '#D6D0C8')
#creating an instance of tkinter.Button() for the bottom
OpenB.pack(in_ = topFrame, side='left')
#putting this thing on screen w/ pack() method

SaveB = tkinter.Button(canvas, text='Save', bg = '#D6D0C8', command= SaveFile)
SaveB.pack(in_ = topFrame, side='left')
#the same

clearB = tkinter.Button(canvas, text='Clear', bg = '#D6D0C8')
clearB.pack(in_ = topFrame, side='left')
#one more

entry = tkinter.Text(canvas, wrap='word', background = '#D4CEC5', font = ('Arial', 12))
entry.pack(padx = 10, pady= 5, expand= True, fill= 'both')

canvas.mainloop()