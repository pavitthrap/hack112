from Tkinter import *
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import cv2
import argparse
import imutils
from collections import deque 
import string
import random
from wikipedia_api_modified import *

#####################################
#         MISC FUNCTIONS            #
#####################################

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

ap = argparse.ArgumentParser() # for deque
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
    data.wordArray = ["CAT", "LOVE", "BIRD", "STONE", "SLOTH"]
    data.imageList = ["wordcat.jpg", "heart.jpg", "bird.jpg", "stones.jpg", "sloth.jpg"]
    data.index = 0
    bubbleinit(data)
    data.isHomeScreen=True
    data.isGameOverLose = False
    data.isGameOverWin = False
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
    data.start=True
    data.options=['New York','Pizza','Gold','Skyscraper','Laptop','Hoodie Allen','Necklace','Chair']

#####################################
#         MODE DISPATCHER           #
#####################################

def mousePressed(event, data):
    if (data.mode == "splash"):     splashMousePressed(event, data)
    elif (data.mode == "tracing"):   tracingMousePressed(event, data)
    elif (data.mode == "bubble"):       bubbleMousePressed(event, data)
    elif (data.mode == "book"):       bookMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splash"):     splashKeyPressed(event, data)
    elif (data.mode == "tracing"):   tracingKeyPressed(event, data)
    elif (data.mode == "bubble"):      bubbleKeyPressed(event, data)
    elif (data.mode == "book"):       bookMousePressed(event, data)

def timerFired(data):
    if (data.mode == "splash"):     splashTimerFired(data)
    elif (data.mode == "tracing"):   tracingTimerFired(data)
    elif (data.mode == "bubble"):      bubbleTimerFired(data)
    elif (data.mode == "book"):       bookTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splash"):     splashRedrawAll(canvas, data)
    elif (data.mode == "tracing"):   tracingRedrawAll(canvas, data)
    elif (data.mode == "bubble"):     bubbleRedrawAll(canvas, data)
    elif (data.mode == "book"):       bookRedrawAll(canvas, data)


#####################################
#         SPLASH SCREEN             #
#####################################

def splashMousePressed(event, data):
    x, y = event.x, event.y
    if (data.width-400 < x < data.width-50) and (150 < y < 200):
        data.mode = "tracing"
    elif (data.width-400 < x < data.width-50) and (250 < y < 300):
        data.mode = "bubble"
    elif (data.width-400 < x < data.width-50) and (350 < y < 400):
        data.mode = "book"
        print("mode book")

def splashKeyPressed(event, data):
    pass

def splashTimerFired(data):
    data.currImg = getImage(data)

def splashRedrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawFakeButtons(canvas, data)
    drawAnImage(canvas)

def drawFakeButtons(canvas, data):
    canvas.create_text(data.width - 220, 100, text="Mode Selection", font="Arial 50 bold")
    canvas.create_rectangle(data.width-400, 150, data.width-50, 200, fill="lightgray", width=0)
    canvas.create_rectangle(data.width-400, 250, data.width-50, 300, fill="lightgray", width=0)
    canvas.create_rectangle(data.width-400, 350, data.width-50, 400, fill="lightgray", width=0)
    canvas.create_text(1175, 175, text="tracing practice", font="Arial 35 bold")
    canvas.create_text(1175, 275, text="bubble pop", font="Arial 35 bold")
    canvas.create_text(1175, 375, text="read a book", font="Arial 35 bold")

def drawAnImage(canvas):

    path = 'FUNWITHWORDS.jpg'
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//3, imageHeight//3
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(1000 + newImageWidth//2, 500 + newImageHeight//2, image = photo)


   
#####################################
#             TRACING               #
#####################################

def tracingMousePressed(event, data):
    x, y = event.x, event.y
    if (data.width-50 > x > data.width-150) and (data.height-20 > y > data.height- 60):
        data.mode = "splash"

def tracingKeyPressed(event, data):
    if event.keysym == 'Right' or event.keysym == 'Down':
        data.index = (data.index + 1)%len(data.wordArray)
        data.pts = deque()
    elif event.keysym == 'Left' or event.keysym=='Up':
        data.index = (data.index-1)%len(data.wordArray)
    if (event.keysym == "space"):
        data.collecting = False if data.collecting else True

def tracingTimerFired(data):
    data.currImg = getImage(data)

def tracingRedrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawWord(canvas, data)
    drawInstructions(canvas, data)
    tracingDrawImage(canvas, 500, 500, data)
    drawBackButton(canvas, data)

def drawWord(canvas, data):
    word = data.wordArray[data.index]
    canvas.create_text(500, 450, text=word, font="Arial 250", stipple="gray50")

def drawInstructions(canvas, data):
    msg = "Use the arrows for a new word!"
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

def drawBackButton(canvas, data):
    canvas.create_rectangle(data.width-50, data.height - 20, data.width-150, data.height-60, fill="lightgray", width=0)
    canvas.create_text(data.width-100, data.height-40, text="BACK", font="Arial 25 bold")

#####################################
#             BUBBLE                #
##################################### 
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

def bubbleMousePressed(event, data):
    x, y = event.x, event.y
    if (data.width-50 > x > data.width-150) and (data.height-20 > y > data.height- 60):
        data.mode = "splash"
    if data.bubbleScreen == data.bubbleLost:
        bubbleinit(data)
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
                

def bubbleKeyPressed(event, data):
    if (event.keysym == "space"):
        data.collecting = False if data.collecting else True
    if data.bubbleScreen == data.bubbleStartMode:
        if event.keysym == "Up": data.bubbleScreen = data.bubblePlay
    if data.bubbleScreen == data.bubblePlay:
        if event.keysym == "r": data.cy = [random.randint(100, 600) for i in range(10)]


def bubbleTimerFired(data):
    data.currImg = getImage(data)
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
    # if data.collecting == True: 
    #     checkIfWon(data)

def bubbleRedrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawBackButton(canvas, data)
    drawBubbleGame(canvas, data)


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

def drawBubbleGame(canvas, data):
    if data.bubbleScreen == data.bubbleStartMode:
        canvas.create_text(300, 100, text = "Press Up Arrow to Start!", 
                            font = "Ariel 40")
    if data.bubbleScreen == data.bubblePlay:
        drawImage(canvas, data.images, 10)
        drawBubbles(canvas, data, data.bubbleLetters)
        canvas.create_text(970, 400, text = data.word, font = "Ariel 30", 
                            fill = "white")
        canvas.create_text(500, 50, text = "Click on the right letters to spell he word. Press r to reset the letter placement", font = "Ariel 20")
    if data.bubbleScreen == data.bubbleLost:
        canvas.create_text(200, 100, text = "You Lose :(", font = "Ariel 40 bold")
        canvas.create_text(500, 350, text = "Click anywere to play again", font = "Ariel 30")
    if data.bubbleScreen == data.bubbleWin:
        canvas.create_text(200, 100, text = "You Win!! :D", 
                            font = "Ariel 40 bold", fill = "lightgreen")
        drawImage(canvas, 'happy.jpg', 2)
        canvas.create_text(500, 350, text = "Click anywere to play again", font = "Ariel 30")

    
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
            for i in range(10): 
                if (data.cx[i]-data.radius < center[0] < data.cx[i]+data.radius or data.cy[i]-data.radius < center[1] < 
                    data.cy[i]+data.radius): 
                    data.result += data.bubbleLetters[i]
                    data.word = data.result
            checkDone(data, data.result)

def drawImage(canvas, path, dividingFactor):
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//dividingFactor, imageHeight//dividingFactor
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(3*newImageWidth, newImageHeight//2, image = photo)
            

#####################################
#             BOOK                  #
##################################### 

def bookMousePressed(event, data):
    x, y = event.x, event.y
    if (data.width-50 > x > data.width-150) and (data.height-20 > y > data.height- 60):
        data.mode = "splash"
        # ignore mousePres  sed events
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
        print("home")
        ifClicked(data,clickX,clickY)
    elif data.isGameScreen:
    
        clickX,clickY=event.x,event.y
        ifClicked2(data,clickX,clickY)
        

def bookKeyPressed(event, data):
    if (event.keysym == 'p'): startGame(data)
    elif (event.keysym == 'h'): openHelpScreen(data) #add an if to make sure hom
    elif (event.keysym == 'space'): resetTime(data)
    elif (event.keysym == 'Tab'): openWinGame(data)
    

def bookTimerFired(data):
    pass

def bookRedrawAll(canvas, data):
    #drawBackground(canvas, data)
    drawBackButton(canvas, data)
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

def ifClicked2(data,x,y):
    left,top,right,bot=50,50,150,100
    if (x>(left) and x<(right)
    and y>(top) and y<(bot)):
        data.isHomeScreen=True
        data.isGameScreen=False

def startGame(data):
    data.isHomeScreen=False 
    data.isGameScreen=True 
    data.wasHomeScreen=False

        
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
    for i in range(len(data.positions)): 
        position=data.positions[i]
        print(position,x,y)
        if (position[0]<x and position[1]>x and position[2]<y and position[3]>y):
            data.selected=data.options[i]
            print("intersec")
            data.isHomeScreen=False
            data.isGameScreen=True
    print(data.isHomeScreen)


#######################################    
def drawHomePage(canvas,data):
    data.text=None
    data.selected=None
    canvas.create_text(data.width/2,data.height/2-data.homeMargin, 
    text="Practice Reading Mode", font="Helvetica %d" % (data.homeScreenSize))
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, 
    text="Input the Wikipedia article you want to read!", font="Helvetica 10")
    #canvas.create_rectangle(data.width/2-data.rectWidth,data.rectY-data.rectHeight,
    #data.width/2+data.rectWidth,data.rectY+data.rectHeight,fill="pink")
    #canvas.create_text(data.width/2, data.rectY, text="Input Article")
    
    margin=5
    initialW=400
    initialH=100
    top=data.rectY+initialH/3
    height=initialH/2
    width=initialW/4
    i=0
    data.positions=[]
    for row in range(2):
        left=data.width/2-initialW/2
        for col in range(4):
           topX,topY=left+margin,top+margin
           botX,botY=left+width-margin,top+height-margin
           position=(topX,botX,topY,botY)
           data.positions.append(position)
           canvas.create_rectangle(topX,topY,botX,botY, fill="pink")
           canvas.create_text((topX+botX)/2,(topY+botY)/2,text=data.options[i])
           left+=width
           i+=1
        top+=height
    data.start=False
    
        
    # book=Entry(canvas)
    # canvas.create_window(data.width/2, data.height/2+60,window=book)
    # canvas.update()

    
def drawHelpScreen(canvas,data):
    data.helpTextX=data.helpTextX+data.increment 
    canvas.create_text(data.helpTextX, data.height/2-data.homeMargin, text=
    "Color in the right bubbles to spell out the word in the picture!", font="Helvetica 11", fill=
    data.helpTextColor)
    canvas.create_text(data.width/2,data.height/2+data.homeMargin, text=
    "Press mouse to return to caller's mode")
    



def drawInstructions(canvas,data):
    canvas.create_text(data.width/2, data.height-data.margin, fill="blue",
    text="Press 'h' for help! Use Space, Tab, MouseButton + Arrows", 
    font="Helvetica 6 bold")

def drawImageBook(canvas, width, height,path):
    image = Image.open(path)
    imageWidth, imageHeight = image.size
    newImageWidth, newImageHeight = imageWidth//3, imageHeight//3
    image = image.resize((newImageWidth, newImageHeight), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo # keep a reference!
    canvas.create_image(newImageWidth//2, newImageHeight//2, image = photo)
#179,204,204
def drawGame(canvas,data):
    #drawImage(canvas,data.width/2,data.height/2,"book2.jpg")
    left,top,right,bot=50,50,150,100
    canvas.create_rectangle(left,top,right,bot,fill="#B3CCCC")
    canvas.create_text((left+right)/2,(top+bot)/2,text="Choose Again")
    if data.text==None:
        data.text=getInput(data.selected)
        data.formatted=formatString(data.text)
        print(data.formatted)
    canvas.create_text(data.width/2,data.height/2-50,text=data.formatted,font="Arial 30")
     #draw book here

def formatString(text):
    if text != None:
        j=0
        newText=""
        for i in range(len(text)):
            if j==50:
                newText+="\n"
                j=0
            j+=1
            newText+=text[i]
        return newText
            


#####################################
#    OPEN CV TKINTER  FUNCTIONS     #
#####################################

def openCVkeyPressed(event, data): 
    if (event.keysym == "space"):
        data.collecting = False if data.collecting else True

def openCVtimerFired(data):
    data.currImg = getImage(data)

def openCVredrawAll(canvas, data):
    drawBackground(canvas, data)
    drawFrame(canvas, data.currImg, data)
    drawImage(canvas, 500, 500)
    drawText(canvas, 500, 500)


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