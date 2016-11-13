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
    return canvas.data.modalResult

def button1Pressed():
    global canvas
    message = "Result = " + str(showDialog(canvas))
    # And update and redraw our canvas
    canvas.data.message = message
    canvas.data.count += 1
    redrawAll(canvas)
    
def redrawAll(canvas):
    canvas.delete(ALL)
    # background (fill canvas)
    if canvas.data.isHomeScreen==True:
        drawHomePage(canvas)
    elif canvas.data.isHelpScreen==True:
        drawHelpScreen(canvas,data)
    elif canvas.data.isGameScreen==True:
        drawGame(canvas)
    canvas.create_rectangle(0,0,300,300,fill="cyan")
    
    #insert redrawll here
def drawHomePage(canvas):
    canvas.create_text(canvas.data.width/2,canvas.data.height/2-canvas.data.homeMargin, 
    text="Practice Reading Mode", font="Helvetica %d" % (canvas.data.homeScreenSize))
    canvas.create_text(canvas.data.width/2,canvas.data.height/2+canvas.data.homeMargin, 
    text="Input the Wikipedia article you want to read!", font="Helvetica 10")
    canvas.create_rectangle(canvas.data.width/2-canvas.data.rectWidth,canvas.data.rectY-canvas.data.rectHeight,
    canvas.data.width/2+canvas.data.rectWidth,canvas.data.rectY+canvas.data.rectHeight,fill="pink")
    canvas.create_text(canvas.data.width/2, canvas.data.rectY, text="Input Article")
    
    # print message
    msg = "message: " + str(canvas.data.message)
    canvas.create_text(150,130,text=msg)
    msg = "count: " + str(canvas.data.count)
    canvas.create_text(150,170,text=msg)
    canvas.pack()
    redrawAll(canvas)

def init(root, canvas):
    canvas.data.message = "none"
    canvas.data.count = 0
    #insert your init here
    canvas.data.isHomeScreen=True
    canvas.data.isGameScreen=False 
    canvas.data.isHelpScreen=False 
    canvas.data.wasGameScreen,canvas.data.wasHelpScreen=False,True
    canvas.data.homeScreenSize=12
    canvas.data.homeMargin,canvas.data.margin=30,10
    canvas.data.helpTextX=canvas.data.width/2
    canvas.data.helpTextColor="black"
    canvas.data.increment=7
    canvas.data.cellWidth,canvas.data.cellHeight=60,60
    canvas.data.currentTime=30
    canvas.data.rectWidth,canvas.data.rectHeight=75,20
    canvas.data.rectY=canvas.data.height/2+75
    #
    buttonFrame = Frame(root)
    b1 = Button(buttonFrame, text="Click here!!!", command=button1Pressed)
    b1.grid(row=0,column=0)
    buttonFrame.pack(side=TOP)
    canvas.pack()
    redrawAll(canvas)




def mousePressed(event, canvas):
    pass
    # ignore mousePres	sed events
    if data.isHelpScreen==True:
        if data.wasGameScreen==False:
            data.isHelpScreen=False
            data.isHomeScreen=True
        else:
            data.isHelpScreen=False
            data.isGameScreen=True
    
    #click on cell 
    elif data.isHomeScreen:
        clickX,clickY=event.x,event.y
        button=ifClicked(data,clickX,clickY)
        if button==True: #open screen
            print("yes")
            createPopUp(data)



def keyPressed(event, canvas):
    pass
    #if (event.keysym == 'r'): init(data)
    # elif (event.keysym == 'Left'): doMove(data, -3, 0)
    # elif (event.keysym == 'Right'): doMove(data, +3, 0)
    # elif (event.keysym == 'Up'): doMove(data, 0, -3)
    # elif (event.keysym == 'Down'): doMove(data, 0, +3)
    if (event.keysym == 'p'): startGame(data)
    elif (event.keysym == 'h'): openHelpScreen(data) #add an if to make sure hom
    elif (event.keysym == 'space'): resetTime(data)
    elif (event.keysym == 'Tab'): openWinGame(data)
    
    

def timerFired(canvas):
    #decrement timer
    pass







########### copy-paste below here ###########
def redrawAll(canvas):
    if canvas.data.isHomeScreen==True:
        drawHomePage(canvas)
    elif canvas.data.isHelpScreen==True:
        drawHelpScreen(canvas)
    elif canvas.data.isGameScreen==True:
        drawGame(canvas)


def run(width=1400,height=800):
    # create the root and the canvas
    root = Tk()
    global canvas # make canvas global for button1Pressed function
    canvas = Canvas(root, width=300, height=300)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct(object): pass
    data = Struct()
    canvas.data = data
    canvas.data.width = width
    canvas.data.height = height
    init(root, canvas)	
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(canvas)
    def redrawAllWrapper(canvas):
        canvas.delete(ALL)
        redrawAll(canvas)
        canvas.update()    

    def mousePressedWrapper(event, canvas):
        mousePressed(event, data)
        redrawAllWrapper(canvas)

    def keyPressedWrapper(event, canvas):
        keyPressed(event, canvas)
        redrawAllWrapper(canvas)

    def timerFiredWrapper(canvas):
        timerFired(data)
        redrawAllWrapper(canvas)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)

    

    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
    print('bye')

def main():
    run()
    

if __name__ == '__main__':
    main()