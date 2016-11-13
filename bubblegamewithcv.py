from tkinter import *
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import cv2
import argparse
from collections import deque 
import random
import string 

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
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
    data.pts = deque(maxlen=args["buffer"]) 
    data.mode = 0
    data.bubbleMode = 1
    bubbleinit(data)

def bubbleinit(data):
    data.cx = [random.randint(100, 800) for i in range(10)]
    data.cy = [random.randint(100, 600) for i in range(10)]
    data.radius = 20
    data.images = 'apple.jpg'
    data.bubbleWords = "APPLE"
    data.bubbleLetters = getLetters(data, data.bubbleWords)
    #data.bubbleLetters2 = getLetters(data, data.bubbleWords[1])
    #data.AllLetters = [data.bubbleLetters1]
    data.bubbleScreen = 0
    data.bubbleWin = -1
    data.bubbleLost = 1
    data.bubblePlay = -2
    data.bubbleStartMode = 0
    data.bubbleDirection = 0
    data.color = ["white"] * 10
    data.result = []
    data.word = ''
    
def getLetters(data, word):
    result = list(word)
    remaining = 10 - len(word)
    for i in range(remaining):
        result += chr(random.randint(ord('A'), ord('U')))
    return result
    
def checkDone(data, result):
    s = list("APPLE")
    count = 0
    for i in range(len(result)):
        if result[i] == s[i]:
            count += 1
            continue
        else:
            data.bubbleScreen = data.bubbleLost
    if count == len(s):
        data.bubbleScreen = data.bubbleWin

def checkIfWon(data):
    (ret, frame) = data.cap.read()
    frame=cv2.flip(frame,1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(cv2image, data.yellowLower, data.yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        if data.bubbleScreen == data.bubblePlay:
            result = []
            for i in range(10): 
                if (data.cx[i]-data.radius < center < data.cx[i]+data.radius or data.cy[i]-data.radius < center < 
                    data.cy[i]+data.radius): 
                    result += data.bubbleLetters1[i] 
            checkDone(data, result)
            
        
def mousePressed(event, data):
    if data.mode == 0:
        data.mode = data.bubbleMode
    if data.mode == data.bubbleMode:
        if data.bubbleScreen == data.bubblePlay:
            for i in range(10):
                if (event.x > data.cx[i] - data.radius and 
                    event.x < data.cx[i] + data.radius and 
                    event.y > data.cy[i] - data.radius and 
                    event.y < data.cy[i] + data.radius):
                        data.color[i] = "blue"
                        data.result += data.bubbleLetters[i]
                        data.word = "".join(data.result)
            checkDone(data, data.result)
                    

def keyPressed(event, data):
    if data.mode == data.bubbleMode:
        if data.bubbleScreen == data.bubbleStartMode:
            if event.keysym == "Up": data.bubbleScreen = data.bubblePlay
            if event.keysym == "r": data.mode = 0
            
def timerFired(data):
    data.currImg = getImage(data)
    if data.mode == data.bubbleMode:
        if data.bubbleScreen == data.bubblePlay:
            for i in range(10):
                if data.bubbleDirection == 0:
                    if data.cy[i] < 725:
                        data.cy[i] += 5
                    else:
                        data.bubbleDirection == 1
                if data.bubbleDirection == 1:
                    if data.cy[i] > 0:
                        data.cy[i] -= 5
                    else:
                        data.bubbleDirection == 0
    checkIfWon(data)
            
    

def drawBubbleGame(canvas, data):
    if data.bubbleScreen == data.bubbleStartMode:
        canvas.create_text(200, 100, text = "Press Up Arrow to Start!", font = "Ariel 40")
    if data.bubbleScreen == data.bubblePlay:
        drawImage(canvas, data.images)
        drawBubbles(canvas, data, data.bubbleLetters)
        canvas.create_text(970, 400, text = data.word, font = "Ariel 30", fill = "white")
    if data.bubbleScreen == data.bubbleLost:
        canvas.create_text(200, 100, text = "You Lose :(", font = "Ariel 40 bold")
    if data.bubbleScreen == data.bubbleWin:
        canvas.create_text(200, 100, text = "You Win!! :D", font = "Ariel 40 bold")
            
def drawBubbles(canvas, data, letters):
    canvas.create_oval(data.cx[0] - data.radius, data.cy[0] - data.radius, data.cx[0] + data.radius, data.cy[0] + data.radius, fill = data.color[0])
    canvas.create_text(data.cx[0], data.cy[0], text = letters[0], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[1] - data.radius, data.cy[1] - data.radius, data.cx[1] + data.radius, data.cy[1] + data.radius, fill = data.color[1])
    canvas.create_text(data.cx[1], data.cy[1], text = letters[1], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[2] - data.radius, data.cy[2] - data.radius, data.cx[2] + data.radius, data.cy[2] + data.radius, fill = data.color[2])
    canvas.create_text(data.cx[2], data.cy[2], text = letters[2], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[3] - data.radius, data.cy[3] - data.radius, data.cx[3] + data.radius, data.cy[3] + data.radius, fill = data.color[3])
    canvas.create_text(data.cx[3], data.cy[3], text = letters[3], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[4] - data.radius, data.cy[4] - data.radius, data.cx[4] + data.radius, data.cy[4] + data.radius, fill = data.color[4])
    canvas.create_text(data.cx[4], data.cy[4], text = letters[4], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[5] - data.radius, data.cy[5] - data.radius, data.cx[5] + data.radius, data.cy[5] + data.radius, fill = data.color[5])
    canvas.create_text(data.cx[5], data.cy[5], text = letters[5], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[6] - data.radius, data.cy[6] - data.radius, data.cx[6] + data.radius, data.cy[6] + data.radius, fill = data.color[6])
    canvas.create_text(data.cx[6], data.cy[6], text = letters[6], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[7] - data.radius, data.cy[7] - data.radius, data.cx[7] + data.radius, data.cy[7] + data.radius, fill = data.color[7])
    canvas.create_text(data.cx[7], data.cy[7], text = letters[7], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[8] - data.radius, data.cy[8] - data.radius, data.cx[8] + data.radius, data.cy[8] + data.radius, fill = data.color[8])
    canvas.create_text(data.cx[8], data.cy[8], text = letters[8], font = "Ariel 30 bold")
    canvas.create_oval(data.cx[9] - data.radius, data.cy[9] - data.radius, data.cx[9] + data.radius, data.cy[9] + data.radius, fill = data.color[9])
    canvas.create_text(data.cx[9], data.cy[9], text = letters[9], font = "Ariel 30 bold")

        
        

def redrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawTitle(canvas, data)
    if data.mode == data.bubbleMode:
        drawBubbleGame(canvas, data)
        

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
        cv2.line(frame, data.pts[i - 1], data.pts[i], (0, 0, 255), thickness)

    finalFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(finalFrame)
    h=675
    desiredW=900
    img=img.crop((0,0,desiredW,h))
    tkImg=ImageTk.PhotoImage(image=img)
    print(data.pts)
    return tkImg

def drawImage(canvas, path):
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//10, imageHeight//10
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(3*newImageWidth, newImageHeight//2, image = photo)



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