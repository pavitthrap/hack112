import Tkinter as tk
import numpy as np
import cv2
from Tkinter import *
from PIL import Image
from PIL import ImageTk

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

    
    
    
def mousepressed(event):
    print(event.x, event.y)




def runDrawing(width=300, height=300):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    drawImage(canvas, width, height)
    drawText(canvas, width, height)
    root.mainloop()
    print("bye!")

runDrawing(500, 400)