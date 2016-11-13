##############################################
## Lab5
##############################################

# from cs112_f16_wk10 import assertEqual, assertAlmostEqual, lintAll, testAll
from wikipedia_api_modified import *
import math, string, copy, random

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Problems
#################################################


##############################################
## ignore_rest: graphics go below here!
##############################################

from tkinter import *


def make2dList(rows, cols, value):
    # helper function to create a 2d list 
    a=[]
    for row in range(rows): a += [[value]*cols]
    return a


def init(data):
    data.isHomeScreen=True
    data.isGameScreen=False 
    data.isHelpScreen=False 
    data.wasGameScreen,data.wasHelpScreen=False,True
    data.homeScreenSize=12
    data.homeMargin,data.margin=30,10
    data.helpTextX=data.width/2
    data.helpTextColor="black"
    data.increment=7
    data.cellWidth,data.cellHeight=60,60
    data.currentTime=30
    data.rectWidth,data.rectHeight=75,20
    data.rectY=data.height/2+75


######################
def mousePressed(event, data):
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



def keyPressed(event, data):
    #if (event.keysym == 'r'): init(data)
    # elif (event.keysym == 'Left'): doMove(data, -3, 0)
    # elif (event.keysym == 'Right'): doMove(data, +3, 0)
    # elif (event.keysym == 'Up'): doMove(data, 0, -3)
    # elif (event.keysym == 'Down'): doMove(data, 0, +3)
    if (event.keysym == 'p'): startGame(data)
    elif (event.keysym == 'h'): openHelpScreen(data) #add an if to make sure hom
    elif (event.keysym == 'space'): resetTime(data)
    elif (event.keysym == 'Tab'): openWinGame(data)
    
    

def timerFired(data):
    #decrement timer
    pass
    
    
        
#################################

def startGame(data):
    data.isHomeScreen=False 
    data.isGameScreen=True 
    data.wasHomeScreen=False


# def resetTime(data):
#     if data.isGameScreen==True:
#         data.currentTime=20
        
# def openWinGame(data):
#     if data.isGameScreen==True:
#         data.isGameScreen=False 
#         data.isGameOverWin=True
        
def openHelpScreen(data):
    if data.isHomeScreen==True:
        data.isHomeScreen=False 
        data.wasHomeScreen=True
        data.isHelpScreen=True
    elif data.isGameScreen==True:
        data.isGameScreen=False 
        data.isHelpScreen=True
        data.wasGameScreen=True
    elif data.isHelpScreen==True:
        if data.wasGameScreen==True:
            data.isHelpScreen=False
            data.isGameScreen=True
        else:
            data.isHelpScreen=False
            data.isHomeScreen=True

def ifClicked(data,x,y):
    if (x>(data.width/2-data.rectWidth) and x<(data.width/2+data.rectWidth)
    and y>(data.rectY-data.rectHeight) and y<(data.rectY+data.rectHeight)):
        return True
    else: return False

def createPopUp(data):
    pass

def show_entry_fields(data):
   print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
   data.article=e1.get()
   master.quit
#######################################    
def drawHomePage(canvas,data,root):
    canvas.create_text(data.width/2,data.height/2-data.homeMargin, 
    text="Practice Reading Mode", font="Helvetica %d" % (data.homeScreenSize))
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, 
    text="Input the Wikipedia article you want to read!", font="Helvetica 10")
    canvas.create_rectangle(data.width/2-data.rectWidth,data.rectY-data.rectHeight,
    data.width/2+data.rectWidth,data.rectY+data.rectHeight,fill="pink")
    canvas.create_text(data.width/2, data.rectY, text="Input Article")
    buttonFrame = Frame(root)
    b1 = Button(buttonFrame, text="Click here!!!", command=button1Pressed)
    b1.grid(row=0,column=0)
    buttonFrame.pack(side=TOP)
    canvas.pack()
    redrawAll(canvas)

    
        
    # book=Entry(canvas)
    # canvas.create_window(data.width/2, data.height/2+60,window=book)
    # canvas.update()

    
def drawHelpScreen(canvas,data):
    canvas.create_text(data.helpTextX, data.height/2-data.homeMargin, text=
    "Color in the right bubbles to spell out the word in the picture!", font="Helvetica 11", fill=
    data.helpTextColor)
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, text=
    "Press mouse to return to caller's mode")
    


def drawTimer(canvas,data):
    displayTime=math.ceil(data.currentTime)
    x0=0
    x1=70
    y0=0
    y1=20
    if data.currentTime<5:
        color="red"
    elif data.currentTime<10:
        color="yellow"
    else:
        color="lightgray"
    canvas.create_rectangle(x0,y0,x1,y1,fill=color)
    canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Timer: %d" %(displayTime))

def drawInstructions(canvas,data):
    canvas.create_text(data.width/2, data.height-data.margin, fill="blue",
    text="Press 'h' for help! Use Space, Tab, MouseButton + Arrows", 
    font="Helvetica 6 bold")


def drawGame(canvas,data):
    pass #draw bubbles here

def drawGameLose(canvas,data):
    canvas.create_text(data.width/2,data.height/2-data.homeMargin,
    text="Game Over!!!", font="Helvetica 20")
    canvas.create_text(data.width/2,data.height/2+data.homeMargin,
    text="You Lose :-(", font="Helvetica 20")

def drawGameWin(canvas,data):
    canvas.create_text(data.width/2,data.height/2-data.homeMargin, 
    text="You Win!!!", font="Helvetica 20")
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, 
    text="Press key or mouse to start over", font="Helvetica 12")

################################3

def redrawAll(canvas, data,root):
    #drawBoard(canvas, data)
    #drawScore(canvas, data)
    if data.isHomeScreen==True:
        drawHomePage(canvas,data,root)
    elif data.isHelpScreen==True:
        drawHelpScreen(canvas,data)
    elif data.isGameScreen==True:
        drawGame(canvas,data)
    elif data.isGameOverLose==True:
        drawGameLose(canvas,data)
    elif data.isGameOverWin==True:
        drawGameWin(canvas,data)
    

def runBook(width=1400, height=800):
    # DO NOT MODIFY THIS FUNCTION!!!!
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    global canvas # make canvas global for button1Pressed function
    canvas = Canvas(root, width=data.width, height=data.height)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    canvas.data["message"] = "none"
    canvas.data["count"] = 0
    canvas.pack()
    data.textvar = StringVar()
    data.start=True
    # set up events
    def redrawAllWrapper(canvas, data,root):
        canvas.delete(ALL)
        redrawAll(canvas, data,root)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data,root)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    
    root.mainloop()  # blocks until window is closed
    print("bye!")

##############################################
## ignore_rest: tests and main go below here
##############################################

#################################################
# Main
#################################################

def main():
    runBook()
    

if __name__ == '__main__':
    main()
