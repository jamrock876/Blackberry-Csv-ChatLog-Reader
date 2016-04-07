from Tkconstants import CENTER

__author__ = 'TheLazySavant'
import math
import Tkinter as tk
import tkFileDialog

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.space = tk.Label(self, width=10, height=15).grid(column=1, row=0)
        self.fileChooserBtn = tk.Button(self, text='Choose File', command=self.filechooser, width=10).grid(column=3, row=2)
        self.openBtn = tk.Button(self, text='Open', command=self.open, width=10, state=tk.DISABLED)
        self.openBtn.grid(column=4, row=2)
        self.lbl = tk.Label(self, text='No File Choosen', width=25)
        self.lbl.grid(column=3, row=1, columnspan=2)
        self.grid()
        self.path = "hello"

    def filechooser(self):
        path = tkFileDialog.askopenfilename()
        if path is not "":
            folders = path.split('/')
            filename = folders[len(folders)-1:]
            self.lbl.config(text='fakepath/'+filename[0])
            self.path = path
            self.openBtn.config(state=tk.NORMAL)

    def open(self):
        self.controller.addSelectPinFrame(self.path)
        self.controller.show_frame(chooseYourPin)

    def parsedate(self):
        print "parse date"

class chatLog(tk.Frame):
    def __init__(self, parent, controller, lines, sender):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.sender = sender
        self.selectedFileLst = lines
        self.maxWidth = 250
        self.leftStartingX = 10.0
        self.startingY = 10.0
        self.rightStartingX = 125.0

        # add scroll bar on the right
        self.scrollpane = tk.Scrollbar(self)
        self.scrollpane.pack(side=tk.RIGHT, fill=tk.Y)

        # scrollable area with each list items
        self.msgbox = tk.Canvas(self, width=370, height=500, bd=5, yscrollcommand=self.scrollpane.set)

        for i in self.dictionaryway():
            # pop text from list
            if i[0] != self.sender:
                # Draw left
                self.l = i[1]
                self.leftbox = self.msgbox.create_rectangle(self.leftStartingX, self.startingY, self.maxWidth, self.getVerticalLength(self.l)+self.startingY, fill="#2087F2")
                self.msgbox.create_text(self.leftStartingX + 8, self.startingY + 5, anchor="nw", font="Purisa", text=self.l, width=230)
                self.startingY += self.getVerticalLength(self.l)+10
            else:
                # Draw Right
                self.r = i[1]
                self.rightbox = self.msgbox.create_rectangle(self.rightStartingX, self.startingY, self.rightStartingX+self.maxWidth, self.getVerticalLength(self.r)+self.startingY, fill="grey")
                self.msgbox.create_text(self.rightStartingX + 8, self.startingY + 5, anchor="nw", font="Purisa", text=self.r, width=230)
                self.startingY += self.getVerticalLength(self.r) + 10

        self.msgbox.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.scrollpane.config(command=self.msgbox.yview)
        self.msgbox.config(scrollregion=self.msgbox.bbox(tk.ALL))

    def getVerticalLength(self, line):
        return (math.ceil(len(line)/35.0))*25

    def dictionaryway(self):
        lst = []
        print self.sender
        print self.selectedFileLst
        for item in self.selectedFileLst[1:]:
            line = item.split(",")
            if len(line) > 3:
                sender = line[1]
                message = ", ".join(line[3:])
                print message
                lst.append([sender[1:-1], message])
        return lst

class chooseYourPin(tk.Frame):
    def __init__(self, parent, controller, path):
        tk.Frame.__init__(self, parent)

        self.selectedFileLst = []
        self.uniquePins = {}
        self.controller = controller
        self.path = path
        self.openFile()
        self.countUniquePins()
        self.lbl = tk.Label(self, text='Select Your Pin', width=25)
        self.lbl.grid(column=3, row=1, columnspan=2)
        self.space = tk.Label(self, width=10, height=15).grid(column=1, row=0)
        self.v = tk.StringVar()
        self.v.set("1") # initialize

        for text, mode in self.uniquePins.items():
            b = tk.Radiobutton(self, text=text, variable=self.v, value=mode)
            # b.pack(anchor='center')
            b.grid(column=3, columnspan=2)

        self.selectBtn = tk.Button(self, text='Select', command=self.confirmSelection, width=10)
        self.selectBtn.grid(column=3)

    def confirmSelection(self):
        self.controller.addNewChatLogFrame(self.selectedFileLst, self.v.get())
        self.controller.show_frame(chatLog)

    # open file and load to
    def openFile(self):
        selectedFile = open(self.path, 'r')
        for line in selectedFile:
            self.selectedFileLst.append(line)
        selectedFile.close()

    def countUniquePins(self):
        val = 0
        for i in self.selectedFileLst[1:]:
            line = i.split(",")
            if len(line) > 3:
                sender = line[1][1:-1]
                if sender not in self.uniquePins:
                    self.uniquePins[sender] = sender
                    val += 1

class PageManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.grid(row=1, column=1)

         # dictionary containing all the frames
        self.frames = {}

        # card layout where all the frames are initialized and placed in a deck format
        for F in (Home,):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def addNewChatLogFrame(self, lines, sender):
        frame = chatLog(self.container, self, lines, sender)

        self.frames[chatLog] = frame

        frame.grid(row=0, column=0, sticky="nsew")

    def addSelectPinFrame(self, path):
        frame = chooseYourPin(self.container, self, path)

        self.frames[chooseYourPin] = frame

        frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = PageManager()
    app.title('BBM ChatLog Reader')
    app.geometry("400x500")
    app.mainloop()
