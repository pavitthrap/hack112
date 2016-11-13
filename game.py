from Tkinter import *
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import cv2
import argparse
import imutils
from collections import deque 

#####################################
#         MISC FUNCTIONS            #
#####################################

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=40,
    help="max buffer size")
args = vars(ap.parse_args())


#####################################
#             INIT                  #
#####################################

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
    data.mode = "splash"
    data.wordArray = ["APPLE", "CAT", "HEART", "BIRD", "STONE"]
    data.imageList = ["apple.jpg", "cat.jpg", "heart.jpg", "bird.jpg", "stones.jpg"]
    data.index = 0

#####################################
#         MODE DISPATCHER           #
#####################################

def mousePressed(event, data):
    if (data.mode == "splash"):     splashMousePressed(event, data)
    elif (data.mode == "tracing"):   tracingMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splash"):     splashKeyPressed(event, data)
    elif (data.mode == "tracing"):   tracingKeyPressed(event, data)
    elif (data.mode == "help"):      helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splash"):     splashTimerFired(data)
    elif (data.mode == "tracing"):   tracingTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splash"):     splashRedrawAll(canvas, data)
    elif (data.mode == "tracing"):   tracingRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)


#####################################
#         SPLASH SCREEN             #
#####################################

def splashMousePressed(event, data):
    x, y = event.x, event.y
    if (data.width-400 < x < data.width-50) and (150 < y < 200):
        data.mode = "tracing"
    elif (data.width-400 < x < data.width-50) and (250 < y < 300):
        pass
        # data.mode = ...
    elif (data.width-400 < x < data.width-50) and (350 < y < 400):
        # data.mode = ...
        print("mode3")

def splashKeyPressed(event, data):
    pass

def splashTimerFired(data):
    data.currImg = getImage(data)

def splashRedrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawTitle(canvas, data)
    drawFakeButtons(canvas, data)
    drawAnImage(canvas)

def drawFakeButtons(canvas, data):
    canvas.create_text(data.width - 220, 100, text="Select a Mode", font="Arial 50 bold")
    canvas.create_rectangle(data.width-400, 150, data.width-50, 200, fill="lightgray", width=0)
    canvas.create_rectangle(data.width-400, 250, data.width-50, 300, fill="lightgray", width=0)
    canvas.create_rectangle(data.width-400, 350, data.width-50, 400, fill="lightgray", width=0)
    canvas.create_text(1175, 175, text=" tracing ", font="Arial 35 bold")
    canvas.create_text(1175, 275, text="MODE 2", font="Arial 35 bold")
    canvas.create_text(1175, 375, text="MODE 3", font="Arial 35 bold")

def drawAnImage(canvas):
    # how to properly resize?
    path = 'bassethound.jpg'
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//3, imageHeight//3
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(900 + newImageWidth//2, 500 + newImageHeight//2, image = photo)
    canvas.create_text(900 + newImageWidth//2, 500 + newImageHeight//2, text = "some relevant image", font = "Arial 20 bold")


   
#####################################
#             TRACING               #
#####################################

def tracingMousePressed(event, data):
    pass

def tracingKeyPressed(event, data):
    if event.keysym == 'Right' or event.keysym == 'Down':
        data.index = (data.index + 1)%len(data.wordArray)
        data.pts = deque()
    elif event.keysym == 'Left':
        data.index = (data.index-1)%len(data.wordArray)


def tracingTimerFired(data):
    data.currImg = getImage(data)

def tracingRedrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    # drawTitle(canvas, data)
    drawWord(canvas, data)
    drawInstructions(canvas, data)
    tracingDrawImage(canvas, 500, 500, data)

def drawWord(canvas, data):
    word = data.wordArray[data.index]
    canvas.create_text(500, 450, text=word, font="Arial 250")

def drawInstructions(canvas, data):
    msg = "Press the right arrow for the next word!"
    canvas.create_text(data.width//2, data.height-25, text=msg, font="Arial 25 bold")

def tracingDrawImage(canvas, imageWidth, imageHeight, data):
    path = data.imageList[data.index]
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//3, imageHeight//3
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(data.width-200, data.height//2, image = photo)


   
#####################################
#         OPEN CV TKINTER           #
#####################################

# ON AND OFF TRACKING
def openCVkeyPressed(event, data): 
    if (event.keysym == "space"):
        data.collecting = False if data.collecting else True

def openCVtimerFired(data):
    data.currImg = getImage(data)

def openCVredrawAll(canvas, data):
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
    (ret, frame) = data.cap.read()
    frame=cv2.flip(frame,1)
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


#####################################
#  RUN FUNCTION (from course notes) #
#####################################

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