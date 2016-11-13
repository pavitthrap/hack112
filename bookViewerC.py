##############################################
## Lab5
##############################################

# from cs112_f16_wk10 import assertEqual, assertAlmostEqual, lintAll, testAll
from wikipedia_api_modified import *
from PIL import Image, ImageTk
import cv2
from Tkinter import *




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
    data.start=True
    data.options=['Water','Pizza','Gold','Einstein','Cellphone','Madrid','Boots','Chair']
    data.selected=data.options[1]

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
        print("home")
        ifClicked(data,clickX,clickY)
    
    elif data.isGameScreen:
        clickX,clickY=event.x,event.y
        ifClicked2(data,clickX,clickY)
        



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

def drawImage(canvas, width, height,path):
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
    j=0
    newText=""
    for i in range(len(text)):
        if j==50:
            newText+="\n"
            j=0
        j+=1
        newText+=text[i]
    return newText
            
        
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
    

def runBook(width=1400, height=800):
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
    data.textvar = StringVar()
    data.start=True
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
    runBook()
    

if __name__ == '__main__':
    main()
