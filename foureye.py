import numpy as np
import cv2
import os
from Tkinter import *
from PIL import Image, ImageTk
import os
import csv

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def init(data):
    data.bgColor=rgbString(179, 204, 204)
    data.width = 1200
    data.height= 800
    data.currImg = None
    cap = cv2.VideoCapture(0)
    data.cap = cap

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.delete(ALL)
    drawBackground(canvas, data)
    data.currImg = getImage(data) 
    drawFrame(canvas, data.currImg, data)

def drawBackground(canvas, data):
    canvas.create_rectangle(0,0,data.width*2,data.height*2,
        fill=data.bgColor,width=0)

def drawFrame(canvas, img, data): # webcam feed 
    # xoffset=300
    # yoffset=200
    xoffset, yoffset =0,0
    canvas.create_image(xoffset,yoffset,anchor=NW,image=img)

def getImage(data): # gets a new frame
    cap = cv2.VideoCapture(0)
    ret,frame=data.cap.read()
    frame=cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img=Image.fromarray(cv2image)
    # h=450
    # desiredW=600
    # img=img.crop((0,0,desiredW,h))
    # convert to tkinter
    tkImg=ImageTk.PhotoImage(image=img)
    return tkImg

####################################
# adapted from course notes
####################################

def run(width=300, height=300):
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
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 200 # milliseconds
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # drawBackground(canvas, data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()