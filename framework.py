from Tkinter import *
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import cv2
import argparse
import imutils
from collections import deque 

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=40,
    help="max buffer size")
args = vars(ap.parse_args())

def init(data):
    data.bgColor=rgbString(179, 204, 204)
    data.width = 1400
    data.height= 800
    cap = cv2.VideoCapture(0)
    data.cap = cap
    data.yellowLower = (20, 100, 100)
    data.yellowUpper = (30, 255, 255)
    data.maxlen = 40
    data.pts= deque(maxlen=args["buffer"]) 
    data.collecting = True

def mousePressed(event, data):
    pass

def keyPressed(event, data): 
    # attempting to turn tracing on and off
    if (event.keysym == "space"):
        data.collecting = False if data.collecting else True
        print (data.collecting)

def timerFired(data):
    data.currImg = getImage(data)

def redrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawTitle(canvas, data)
    drawImage(canvas, 500, 500)
    drawText(canvas, 500, 500)
    drawLetter(canvas)

def drawTitle(canvas, data):
    canvas.create_text(data.width//2, data.height-30, text="TITLE", font="Arial 65 bold")

def drawBackground(canvas, data):
    canvas.create_rectangle(0,0,data.width*2,data.height*2,
        fill=data.bgColor,width=0)

def drawFrame(canvas, img, data): # draws each webcam frame
    xoffset, yoffset = 50, 50
    canvas.create_image(xoffset,yoffset,anchor=NW,image=img)

def getImage(data): # gets a new frame
    (ret, frame) = data.cap.read()
    frame=cv2.flip(frame,1)

    ############################
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    mask = cv2.inRange(cv2image, data.yellowLower, data.yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    data.pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(data.pts)):
        # if either of the tracked points are None, ignore
        # them
        if data.pts[i - 1] is None or data.pts[i] is None:
            continue
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        if data.collecting == True: 
            cv2.line(frame, data.pts[i - 1], data.pts[i], (0, 0, 255), thickness)
    if data.collecting == False: 
        data.pts = deque(maxlen=args["buffer"]) 


    finalFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(finalFrame)
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
    data.timerDelay = 0 # milliseconds
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