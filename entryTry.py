# dialogs-demo2.py
# modal dialog, text input field, and hidden password

from Tkinter import *
import tkMessageBox
import tkSimpleDialog

class MyDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        canvas.data["modalResult"] = None
        Label(master, text="User:").grid(row=0)
        Label(master, text="Password:").grid(row=1)
        self.e1 = Entry(master)
        self.e2 = Entry(master, show="*")
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus
    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        global canvas
        canvas.data["modalResult"] = (first, second)

def showDialog(canvas):
    MyDialog(canvas)
    return canvas.data["modalResult"]

def button1Pressed():
    global canvas
    message = "Result = " + str(showDialog(canvas))
    # And update and redraw our canvas
    canvas.data["message"] = message
    canvas.data["count"] += 1
    redrawAll(canvas)
    
def redrawAll(canvas):
    canvas.delete(ALL)
    # background (fill canvas)
    canvas.create_rectangle(0,0,300,300,fill="cyan")
    # print message
    msg = "message: " + str(canvas.data["message"])
    canvas.create_text(150,130,text=msg)
    msg = "count: " + str(canvas.data["count"])
    canvas.create_text(150,170,text=msg)

def init(root, canvas):
    canvas.data["message"] = "none"
    canvas.data["count"] = 0
    buttonFrame = Frame(root)
    b1 = Button(buttonFrame, text="Click here!!!", command=button1Pressed)
    b1.grid(row=0,column=0)
    buttonFrame.pack(side=TOP)
    canvas.pack()
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    global canvas # make canvas global for button1Pressed function
    canvas = Canvas(root, width=300, height=300)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(root, canvas)	
    # set up events
    #root.bind("<Button-1>", mousePressed)
    #root.bind("<Key>", keyPressed)
    #timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()