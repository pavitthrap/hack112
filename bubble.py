##############################################
## Lab5
##############################################

# from cs112_f16_wk10 import assertEqual, assertAlmostEqual, lintAll, testAll
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
import Tkinter as tk
import numpy as np
import cv2
from Tkinter import *
from PIL import Image
from PIL import ImageTk


def make2dList(rows, cols, value):
    # helper function to create a 2d list 
    a=[]
    for row in range(rows): a += [[value]*cols]
    return a


def init(data):
    data.isHomeScreen=True
    data.isGameScreen=False 
    data.isGameOverWin=False 
    data.isGameOverLose=False 
    data.isHelpScreen=False 
    data.wasGameScreen,data.wasHelpScreen=False,True
    data.homeScreenSize=12
    data.homeMargin,data.margin=30,10
    data.helpTextX=data.width/2
    data.helpTextColor="black"
    data.increment=7
    data.cellWidth,data.cellHeight=60,60
    data.currentTime=30

######################
def mousePressed(event, data):
    if data.isGameOverWin: init(data)
    # ignore mousePres	sed events
    if data.isHelpScreen==True:
        if data.wasGameScreen==False:
            data.isHelpScreen=False
            data.isHomeScreen=True
        else:
            data.isHelpScreen=False
            data.isGameScreen=True
    
    #click on cell 
    elif data.isGameScreen:
        clickX,clickY=event.x,event.y
        getClickedCell(data,clickX,clickY)



def keyPressed(event, data):
    if data.isGameOverWin: init(data)
    if (event.keysym == 'r'): init(data)
    # elif (event.keysym == 'Left'): doMove(data, -3, 0)
    # elif (event.keysym == 'Right'): doMove(data, +3, 0)
    # elif (event.keysym == 'Up'): doMove(data, 0, -3)
    # elif (event.keysym == 'Down'): doMove(data, 0, +3)
    elif (event.keysym == 'p'): startGame(data)
    elif (event.keysym == 'h'): openHelpScreen(data) #add an if to make sure hom
    elif (event.keysym == 'space'): resetTime(data)
    elif (event.keysym == 'Tab'): openWinGame(data)
    
    

def timerFired(data):
    #decrement timer
    if data.isGameScreen==True:
        if data.currentTime<=0: 
            data.isGameScreen=False
            data.isGameOverLose=True
        else: data.currentTime-=.1
    
    
        
#################################

def startGame(data):
    data.isHomeScreen=False 
    data.isGameScreen=True 
    data.wasHomeScreen=False


def resetTime(data):
    if data.isGameScreen==True:
        data.currentTime=20
        
def openWinGame(data):
    if data.isGameScreen==True:
        data.isGameScreen=False 
        data.isGameOverWin=True
        
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
# 
# def doMove(data, dx, dy):
#     if data.isGameScreen !=False:
#         data.currentX=data.currentX+dx
#         data.currentY=data.currentY+dy
#         checkCurrentCell(data)

# def getClickedCell(data,x,y): 
#     row,col=0,0
#     boardX=(x-data.width/2)+data.currentX
#     boardY=(y-data.height/2)+data.currentY
#     while (boardX>row*data.cellWidth and boardX<
#     data.rows*data.cellWidth): #find col position
#         row+=1
#     while(boardY>col*data.cellHeight and boardY<
#     data.cols*data.cellHeight):
#         col+=1
#     if col!=0 and row!=0: #if it's a valid cell, change score & current cell
#         data.board[row-1][col-1]+=1
#         data.currentCell=[row-1,col-1]
#     data.currentX=boardX
#     data.currentY=boardY
#        
# 
# def checkCurrentCell(data): 
#     row,col=0,0
#     while (data.currentX>row*data.cellWidth and data.currentX<
#     data.rows*data.cellWidth):
#         row+=1
#     #if its 0 disregard, because it's out of bounds
#     #else subtract 1 to get real row 
#     while(data.currentY>col*data.cellHeight and data.currentY<
#     data.cols*data.cellHeight):
#         col+=1
#     #disregard col=0
#     if col!=0 and row!=0:
#         if [row-1,col-1]!=data.currentCell:
#             data.board[row-1][col-1]+=1
#             data.currentCell=[row-1,col-1]

#######################################    
def drawHomePage(canvas,data):
    canvas.create_text(data.width/2,data.height/2-data.homeMargin, 
    text="The Bubble Game", font="Helvetica %d" % (data.homeScreenSize))
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, 
    text="Press 'p' to play, 'h' for help!", font="Helvetica 10")

def drawHelpScreen(canvas,data):
    data.helpTextX=data.helpTextX+data.increment 
    canvas.create_text(data.helpTextX, data.height/2-data.homeMargin, text=
    "Color in the right bubbles to spell out the word in the picture!", font="Helvetica 11", fill=
    data.helpTextColor)
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, text=
    "Press mouse to return to caller's mode")
    

# def drawCell(canvas, data, row, col):
#     x0=data.width/2-data.currentX+row*data.cellWidth
#     y0=data.height/2-data.currentY+col*data.cellHeight
#     x1=x0+data.cellWidth
#     y1=y0+data.cellHeight
#     color=data.fillCell
#     if [row,col]==data.currentCell:
#         if color=="lightyellow":
#             color="yellow"
#         elif color=="lightblue":
#             color="blue"
#     canvas.create_rectangle(x0,y0,x1,y1,fill=color)
#     canvas.create_text((x0+x1)/2,(y0+y1)/2-data.margin,text="(%d,%d)"%(row,col))
#     canvas.create_text((x0+x1)/2,(y0+y1)/2+data.margin,text="%d"%
#     (data.board[row][col]))
# 
# def drawBoard(canvas, data):
#     for row in range(data.rows):
#         data.fillCell="lightyellow" if row%2==0 else "lightblue"
#         for col in range(data.cols):
#             drawCell(canvas, data, row, col)
#             data.fillCell=("lightblue" if data.fillCell=="lightyellow" 
#             else "lightyellow")
# 
# def drawRedDot(canvas,data):
#     data.dotRadius=5
#     x0=data.width/2-data.dotRadius
#     y0=data.height/2-data.dotRadius
#     x1=data.width/2+data.dotRadius
#     y1=data.height/2+data.dotRadius
#     canvas.create_oval(x0,y0,x1,y1,fill="red")

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

def redrawAll(canvas, data):
    #drawBoard(canvas, data)
    #drawScore(canvas, data)
    if data.isHomeScreen==True:
        drawHomePage(canvas,data)
    elif data.isHelpScreen==True:
        drawHelpScreen(canvas,data)
    elif data.isGameScreen==True:
        drawGame(canvas,data)
    elif data.isGameOverLose==True:
        drawGameLose(canvas,data)
    elif data.isGameOverWin==True:
        drawGameWin(canvas,data)
    

def runGameLikeApp(width=300, height=300):
    # DO NOT MODIFY THIS FUNCTION!!!!
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
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
    runGameLikeApp()
    

if __name__ == '__main__':
    main()
