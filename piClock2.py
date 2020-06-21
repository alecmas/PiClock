from os import walk
import socket
from tkinter import *
from time import strftime
from PIL import ImageTk, Image
from itertools import cycle
import time  # TODO: clean up imports
from random import seed
from random import randint

# INSTRUCTIONS:
# press/click to open menu

# set to "on" to enable logging
debugMode = "off"

# Create any needed global variables
pictureMode = 0  # Picture Types, 0 = Pictures with Numbers, 1 = Pictures without Numbers
seed(1)

# create tkinter window
root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

# initialize window dimensions and position variables
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xWindowPos = 0
yWindowPos = 0

if (debugMode == "on"):
    screenHeight = screenHeight / 2
    screenWidth = screenWidth / 2
    yWindowPos = screenHeight / 2

digitMaxSize = (round(screenWidth / 4, 0), round(screenHeight, 0))  # maximum size of a given digit

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (screenWidth, screenHeight, xWindowPos, yWindowPos))

# remove borders on window
root.overrideredirect(True)

# create a canvas
canvas = Canvas(root, bg="white")
canvas.grid(row=0, column=0, sticky="NESW")
Grid.rowconfigure(canvas, 0, weight=1)
Grid.columnconfigure(canvas, 0, weight=1)

# default image paths
backgroundPath = "./images/backgrounds"
numberPath = "./images/numbers"
numberedPhotosPath = "./images/numberedPhotos"

# backgrounds for layered mode
f = []
for (dirPath, dirNames, fileNames) in walk(backgroundPath):
    f.extend(fileNames)
    break
if (debugMode == "on"):
    print("Layered backgrounds: " + str(dirNames))

# styles for simple mode
f = []
for (numberedDirPath, numberedDirNames, numberedFileNames) in walk(numberedPhotosPath):
    f.extend(numberedFileNames)
    break
if (debugMode == "on"):
    print("Simple styles: " + str(numberedDirNames))

styleList = dirNames
# iterator for style list
styleCycle = cycle(styleList)
# default style to first one
style = next(styleCycle)

numberedStyleList = numberedDirNames
# iterator for style list
numberedStyleCycle = cycle(numberedStyleList)
# default style to first one
numberedStyle = next(numberedStyleCycle)

# initialize images to default style
canvas.image0 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))
canvas.image1 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))
canvas.image2 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))
canvas.image3 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))
canvas.image4 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))
canvas.image5 = ImageTk.PhotoImage(Image.open(numberPath + "/0.png"))

# put images in list for easier modification later
imageList = [canvas.image0,
             canvas.image1,
             canvas.image2,
             canvas.image3,
             canvas.image4,
             canvas.image5]

# put images in list for easier modification later
junk = [canvas.image0,
        canvas.image1,
        canvas.image2,
        canvas.image3,
        canvas.image4,
        canvas.image5]

# get image corresponding to number - This routine used for photos that already have numbers, e.g. NBA jerseys (Mode 1)
def getNumberPath(number):
    switcher = {}
    for i in range(10):
        switcher[str(i)] = numberedPhotosPath + "/" + numberedStyle + "/" + str(i) + ".jpg"
        img = Image.open(numberedPhotosPath + "/" + numberedStyle + "/" + str(i) + ".jpg")

    return switcher.get(number, "invalid image number")


# get image corresponding to number - This routine used to get numbers for photos without numbers, e.g. Family Pics (Mode 0)
def getNumberImagePath(number):
    switcher = {}
    for i in range(10):
        switcher[str(i)] = numberPath + "/" + str(i) + ".png"
        img = Image.open(numberPath + "/" + str(i) + ".png")

    return switcher.get(number, "invalid image number")


# get image corresponding to number
def getBackgroundImagePath(number):
    switcher = {}

    f = []
    for (dirpath, dirnames, filenames) in walk(backgroundPath + "/" + style):
        f.extend(filenames)
        break

    for i in range(10):
        switcher[str(i)] = backgroundPath + "/" + style + "/" + filenames[randint(0, len(filenames) - 1)]

    return switcher.get(number, "invalid image number")


def refreshMode0Time():
    canvas.delete("all")
    timeString = strftime("%I%M%S")

    xPos = 0
    for i in range(4):
        imageList[i] = Image.open(getNumberPath(timeString[i]))
        imageList[i].thumbnail(digitMaxSize)
        imageList[i] = ImageTk.PhotoImage(imageList[i])
        canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
        xPos += round(screenWidth / 4, 0)


# clears canvas and refreshes the time and time images
def refreshMode1Time():
    global img
    global junk

    canvas.delete("all")
    timeString = strftime("%I%M%S")

    xPos = 0
    percent = 1
    for i in range(4):
        # Open the BackgroundImageList Image - fixed to "BackgroundImageList" for now
        # Get the BackgroundImageList dimensions - should be 512 x 600
        BackgroundImage = (Image.open(getBackgroundImagePath(timeString[i])))

        BackgroundImage.thumbnail(digitMaxSize)
        bwidth, bheight = BackgroundImage.size
        
        # Get the dimensions of the foreground image (the digit)
        imageList[i] = (Image.open(getNumberImagePath(timeString[i])))
        imwidth, imheight = imageList[i].size
        
        # Paste the foreground onto the BackgroundImageList
        BackgroundImage.paste(imageList[i], (int(bwidth / 2 - imwidth / 2), bheight - imheight - 10), imageList[i])
        junk[i] = ImageTk.PhotoImage(BackgroundImage)
        
        canvas.create_image(xPos, screenHeight, image=junk[i], anchor='sw')
        xPos += round(screenWidth / 4, 0)


# main clock function loop which refreshes every 1 sec
def clock():
    if pictureMode == 0:
        refreshMode0Time()
    else:
        refreshMode1Time()
    canvas.after(5000, clock)


# enable changing of Picture Modes
def changePictureMode(changeStyleButton, changeModeButton):
    global pictureMode
    
    if pictureMode == 0:
        pictureMode = 1
        refreshMode1Time()
        changeStyleButton.config(text="Change Photo Style: " + style)
    else:
        pictureMode = 0
        refreshMode0Time()
        changeStyleButton.config(text="Change Photo Style: " + numberedStyle)
        
    changeModeButton.config(text="Change Photo Mode: " + str(pictureMode))

# enable changing of styles
def changeStyle(button):
    global style
    global numberedStyle
    
    style = next(styleCycle)
    numberedStyle = next(numberedStyleCycle)
    
    if pictureMode == 0:
        refreshMode0Time()
        button.config(text="Change Photo Style: " + numberedStyle)
    else:
        refreshMode1Time()
        button.config(text="Change Photo Style: " + style)
        

def quitProgram():
    root.destroy()
    sys.exit()

def closeMenu(menuCanvas):
     menuCanvas.destroy()
     
def openMenu(event):
    menuCanvas = Canvas(canvas, bg="white")
    menuCanvas.grid(row=0, column=0, sticky="NESW")
    
    for row_index in range(4):
        Grid.rowconfigure(menuCanvas, row_index, weight=1)
        for col_index in range(2):
            Grid.columnconfigure(menuCanvas, col_index, weight=1)
            
    if pictureMode == 0:
        currentStyle = numberedStyle
    else:
        currentStyle = style
    
    quitButton = Button(menuCanvas, text="Quit Program", command=quitProgram)
    closeMenuButton = Button(menuCanvas, text="Close Menu", command=lambda: closeMenu(menuCanvas))
    changeStyleButton = Button(menuCanvas, text="Change Photo Style: " + currentStyle, command=lambda: changeStyle(changeStyleButton))
    changeModeButton = Button(menuCanvas, text="Change Photo Mode: " + str(pictureMode), command=lambda: changePictureMode(changeStyleButton, changeModeButton))
    
    quitButton.grid(row=0, column=0, sticky="NESW")
    closeMenuButton.grid(row=1, column=0, sticky="NESW")
    changeStyleButton.grid(row=0, column=1, sticky="NESW")
    changeModeButton.grid(row=1, column=1, sticky="NESW")
    
# bind screen press for menu open
canvas.bind("<ButtonPress-1>", openMenu)

# run time function
clock()

# Driver code
if (debugMode == "on"):
    print("Screen Size: " + str(screenWidth) + " x " + str(screenHeight))
    
    (digitMaxWidth, digitMaxHeight) = digitMaxSize
    print("Digit Size: " + str(digitMaxWidth) + " x " + str(digitMaxHeight))
        
    try:
        hostName = socket.gethostname()
        hostIP = socket.gethostbyname(hostName)
        print("Hostname:  ", hostName)
        print("IP: ", hostIP)
    except:
        print("Unable to get Hostname and IP")

# infinite running loop
root.mainloop()