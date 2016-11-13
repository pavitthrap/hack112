from Tkinter import *
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import cv2

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def init(data):
    data.bgColor=rgbString(179, 204, 204)
    data.width = 1400
    data.height= 800
    cap = cv2.VideoCapture(0)
    data.cap = cap

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    data.currImg = getImage(data)

def redrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawTitle(canvas, data)
    drawImage(canvas, 500, 500)
    drawText(canvas, 500, 500)

def drawTitle(canvas, data):
    canvas.create_text(data.width//2, data.height-30, text="TITLE", font="Arial 65 bold")

def drawBackground(canvas, data):
    canvas.create_rectangle(0,0,data.width*2,data.height*2,
        fill=data.bgColor,width=0)

def drawFrame(canvas, img, data): # draws each webcam frame
    xoffset, yoffset = 50, 50
    canvas.create_image(xoffset,yoffset,anchor=NW,image=img)

def getImage(data): # gets a new frame
    ret,frame=data.cap.read()
    frame=cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img=Image.fromarray(cv2image)
    h=675
    desiredW=900
    img=img.crop((0,0,desiredW,h))
    tkImg=ImageTk.PhotoImage(image=img)
    return tkImg

def drawImage(canvas, width, height):
    path = 'bassethound.jpg'
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//3, imageHeight//3
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(newImageWidth//2, newImageHeight//2, image = photo)

def drawText(canvas, width, height):
    canvas.create_text(width/2, height/2, text = "W o r d", font = "Ariel 40 bold")


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
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
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
    root.mainloop()  
    print("closed without crashing!")

run()