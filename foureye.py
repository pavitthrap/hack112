# events-example0.py
# Barebones timer, mouse, and keyboard events
import Tkinter as tk
import cv2
import os
from Tkinter import *
from PIL import Image, ImageTk
import os
import csv
# import webbrowser

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

####################################
# customize these functions
####################################

def init(data):
    data.backgroundColor=rgbString(45,51,98)
    data.offset = 50

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
    updateAll(canvas, data)

def drawBackground(canvas, data):
    rectW,rectH=1200,800
    offset=data.offset
    canvas.create_rectangle(0,0,rectW*2,rectH*2,
        fill=data.backgroundColor,width=0)

def drawFrame(canvas,img): # webcam feed 
    xoffset=100
    yoffset=200
    canvas.create_image(xoffset,yoffset,anchor=NW,image=img)


def updateImage(data):
    #gets new frame from webcam feed every time it's called
    cap = cv2.VideoCapture(0)
    ret,frame=data.cap.read()
    frame=cv2.flip(frame,1)
    if data.pause==True: data.cv2img=frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img=Image.fromarray(cv2image)
    h=450
    desiredW=600
    img=img.crop((0,0,desiredW,h))
    # convert to tkinter
    tkImg=ImageTk.PhotoImage(image=img)
    return tkImg

def updateAll(canvas, data):
    #continually updates the entire screen and draws all
    img = updateImage(data)
    if data.pause==True: #checks for paused images
        if data.pauseImg==None:
            data.pauseImg=img
        drawFrame(canvas,data.pauseImg)
        redrawAll(canvas)
    else:
        data.currImg=img
        redrawAll(canvas, data)
    framerate=5
    canvas.after(framerate,func=lambda:updateAll(canvas, data))

def reset(data):
    #starts all the booleans that tells us where in the program we are
    cap = cv2.VideoCapture(0) #gives a video feed
    data.cap=cap
    imgwidth,imgheight=800,450
    data.cap.set(3, imgwidth) #sets the size of the video feed
    data.cap.set(4, imgheight)
    data.pause=False #the image isn't paused
    w,h=1200,800
    data.width,data.height=w,h #width and height of the screen
    #sets up colors for the program 
    data.backgroundColor=rgbString(66,51,98)
    data.accentColor=rgbString(195,186,235)
    data.highlightColor=rgbString(255,255,255)
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        # canvas.create_rectangle(0, 0, data.width, data.height,
        #                         fill='white', width=0)
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
    reset(data)
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    canvas.after(0,func=lambda:updateAll(canvas, data)) #continually updates 

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 500)