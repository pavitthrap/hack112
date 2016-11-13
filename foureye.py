def updateTryOnImage(): #gets new frame from webcam feed every time it's called
    cap=cv2.VideoCapture(0)
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    ret,img=cap.read()
    frame=cv2.flip(img,1)
    data.frameCounter=0
    eyes="source/haarcascades/haarcascade_eye.xml"
    face="source/haarcascades/haarcascade_frontalface_alt.xml"
    data.eyeCascade=cv2.CascadeClassifier(eyes)
    data.faceCascade=cv2.CascadeClassifier(face)
    data.glassesx,data.glassesy=getEyeXAndY(frame)
    data.glassesScale=getGlassesScale(frame)
    frame=putOnGlasses(frame) 
    frame=cv2.resize(frame,(0,0),fx=0.59,fy=0.59)
    data.savedImage=frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img=Image.fromarray(cv2image)
    data.firstFrame=False
    tkImg=ImageTk.PhotoImage(image=img) #converts to tkinter image
    data.pausedTryOnImage=tkImg
    data.imageLabel._image_cache=tkImg
    data.frameCounter+=1
    return tkImg

def updateImage():
    #gets new frame from webcam feed every time it's called
    ret,frame=data.cap.read()
    frame=cv2.flip(frame,1)
    if data.pause==True: data.cv2img=frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img=Image.fromarray(cv2image)
    h=450
    desiredW=600
    img=img.crop((0,0,desiredW,h))
    #converts to tkinter image
    tkImg=ImageTk.PhotoImage(image=img)
    data.imageLabel._image_cache=tkImg
    return tkImg

def updateAll(canvas):
    #continually updates the entire screen and draws all
    img = updateImage()
    if data.pause==True: #checks for paused images
        if data.pauseImg==None:
            data.pauseImg=img
        drawFrame(canvas,data.pauseImg)
        if data.dots==None: 
            data.facerect=detectFace(data.cv2img)
            data.dots=makeDots()
        drawAll(canvas)
    else:
        data.currImg=img
        drawAll(canvas)
    framerate=5
    canvas.after(framerate,func=lambda:updateAll(canvas))


###########draw functions
def drawBackground(canvas):
    #draws the purple area in the back of each screen
    data.backgroundColor=rgbString(66,51,98)
    rectW,rectH=1200,800
    data.offset=50
    offset=data.offset
    canvas.create_rectangle(0,0,rectW*2,rectH*2,
        fill=data.backgroundColor,width=0)

def drawFrame(canvas,img):
    #draws the webcam feed
    xoffset=100
    yoffset=209
    canvas.create_image(xoffset,yoffset,anchor=NW,image=img)

def drawStartScreen(canvas):
    #sets up size of the button
    #draws the background
    #canvas.create_rectangle(0,0,data.width*2,data.height*2,
       # fill=data.backgroundColor,width=0)
    mainText="FourEyes"
    font="Avenir 125 bold"
    #draws the title
    canvas.create_text(data.width/2,data.height/4,anchor="c",
        fill=data.highlightColor,text=mainText,font=font)
    filler1="Learn which glasses frames will look"
    filler2="the best with your face shape."
    font="Avenir 34"
    #draws the descriptions
    canvas.create_text(data.width/2,1.65*data.height/4-5,anchor="c",
        fill=data.accentColor,text=filler1,font=font)
    canvas.create_text(data.width/2,1.9*data.height/4-5,anchor="c",
        fill=data.accentColor,text=filler2,font=font)
    data.startButton.draw(canvas)
