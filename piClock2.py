from os import walk
# import numpy
import socket
from tkinter import * 
from tkinter.ttk import *
from time import strftime 
from PIL import ImageTk, Image
from itertools import cycle
import time # TODO: clean up imports
from random import seed
from random import randint

# INSTRUCTIONS:
# press/click once to change style
# press/hold for 5 seconds to exit clock

# Create any needed global variables
timeCheck = 0
seed(1)


# creating tkinter window
root = Tk()
w = root.winfo_screenwidth()  # width for the Tk root
h = 600 # height for the Tk root
DigitMaxSize = (round(w / 4,0), round(h,0)) #maximum size of a given digit

# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()


# calculate x and y coordinates for the Tk root window
x = 0
y = 0

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# for removing borders on window
root.overrideredirect(True) 

# create frame within root window to hold clock images
clockFrame = Frame(root)
clockFrame.pack()

# create a canvas
canvas = Canvas(clockFrame, bg="black", width=2048, height=600, highlightthickness=0)

# default image path
Picturemode = 0 #Picture Types, 0 = Pictures with Numbers, 1 = Pictures without Numbers
BackgroundPath = "./images/backgrounds"
NumberPath = "./images/Numbers"
NumberedPhotosPath = "./images/NumberedPhotos"

# create list of contents in imagepPath: dirnames = directories
f = []
for (dirpath, dirnames, filenames) in walk(BackgroundPath):
    f.extend(filenames)
    break    
print(dirnames)

f = []
for (Numbereddirpath, Numbereddirnames, Numberedfilenames) in walk(NumberedPhotosPath):
    f.extend(Numberedfilenames)
    break
print(Numbereddirnames)

styleList = dirnames
# iterator for style list
styleCycle = cycle(styleList)
# default style to first one
style = next(styleCycle)

NumberedstyleList = Numbereddirnames
# iterator for style list
NumberedstyleCycle = cycle(NumberedstyleList)
# default style to first one
Numberedstyle = next(NumberedstyleCycle)


# initialize images to default style
canvas.image0 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))
canvas.image1 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))
canvas.image2 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))
canvas.image3 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))
canvas.image4 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))
canvas.image5 = ImageTk.PhotoImage(Image.open("./images/Numbers/0.png"))

# put images in list for easier modification later
imageList = [canvas.image0,
            canvas.image1,
            canvas.image2,
            canvas.image3,
            canvas.image4,
            canvas.image5]

# put images in Backgroun list for easier modification later
junk = [canvas.image0,
            canvas.image1,
            canvas.image2,
            canvas.image3,
            canvas.image4,
            canvas.image5]

# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP")


# get image corresponding to number - This routine used for photos that already have numbers, e.g. NBA jerseys (Mode 1)
def getNumberPath(number):
    switcher = {}
    for i in range(10):
        switcher[str(i)] = NumberedPhotosPath + "/" + Numberedstyle + "/" + str(i) + ".jpg"
        img = Image.open(NumberedPhotosPath + "/" + Numberedstyle + "/" + str(i) + ".jpg")

    return switcher.get(number, "invalid image number")


# get image corresponding to number - This routine used to get numbers for photos without numbers, e.g. Family Pics (Mode 0)
def getNumberImagePath(number):
    switcher = {}
    for i in range(10):
        # BackgroundImageList = imagePath + style + "/" + str(i) + "BackgroundImageList.jpg"
        switcher[str(i)] = NumberPath + "/" + str(i) + ".png"
        img = Image.open(NumberPath + "/" + str(i) + ".png")
        
    return switcher.get(number, "invalid image number")

# get image corresponding to number
def getBackgroundImagePath(number):
    switcher = {}

    f = []
    for (dirpath, dirnames, filenames) in walk(BackgroundPath+"/"+style):
        f.extend(filenames)
        break    
    # print(filenames)
    # print(len(filenames))
    
    for i in range(10):
        switcher[str(i)] = BackgroundPath + "/" + style + "/" + filenames[randint(0,len(filenames)-1)]
       
    return switcher.get(number, "invalid image number")


def refreshMode0Time():
    canvas.delete("all")
    timeString = strftime("%I%M%S")

    xPos = 0
    for i in range(4):
        imageList[i] = Image.open(getNumberPath(timeString[i]))
        imageList[i].thumbnail(DigitMaxSize)
        imageList[i] = ImageTk.PhotoImage(imageList[i])
        canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
        xPos += round(w/4,0)


# clears canvas and refreshes the time and time images
def refreshMode1Time():
    global img
    global junk
    global w

    canvas.delete("all")
    timeString = strftime("%I%M%S")
   
    xPos = 0
    percent = 1
    for i in range(4):
        # Open the BackgroundImageList Image - fixed to "BackgroundImageList" for now
        # Get the BackgroundImageList dimensions - should be 512 x 600
        BackgroundImage = (Image.open(getBackgroundImagePath(timeString[i])))
        
        BackgroundImage.thumbnail(DigitMaxSize)
        bwidth, bheight = BackgroundImage.size
        # print(BackgroundImage.size)
        # Get the dimensions of the foreground image (the digit)
        imageList[i] = (Image.open(getNumberImagePath(timeString[i])))
        imwidth, imheight = imageList[i].size
        # Paste the foreground onto the BackgroundImageList
        BackgroundImage.paste(imageList[i], (int(bwidth/2-imwidth/2),bheight - imheight - 10), imageList[i])
        junk[i]=ImageTk.PhotoImage(BackgroundImage)
        #canvas.create_image(xPos, 0, image=junk, anchor='nw')
        canvas.create_image(xPos,600,image=junk[i], anchor='sw')
        xPos += round(w/4,0)
        # print ("xPos:",xPos)
        
# main clock function loop which refreshes every 1 sec
def clock(): 
    global timeCheck
    if Picturemode == 0:
        refreshMode0Time()
    else:
        refreshMode1Time()
    canvas.after(5000, clock)

# enable changing of Picture Modes
def changePictureMode():
    global Picturemode
    Picturemode += 1
    if Picturemode > 3: Picturemode = 0

# enable changing of styles
def changeStyle():
    global style
    global Numberedstyle
    style = next(styleCycle)
    Numberedstyle = next(NumberedstyleCycle)
    if Picturemode == 0:
        refreshMode0Time()
    else:
        refreshMode1Time()

########################### MENU SYSTEM ###########################
# TODO: extract menu system into a separate package/library?
def pressButton(button):
    button.configure(bg="grey")

def releaseChangeStyleButton(button, label, menu):
    button.configure(bg="white")
    changeStyle()
    menu.itemconfig(label, text="Current Style: " + style)

def releaseChangePictureModeButton(button, label, menu):
    button.configure(bg="white")
    changePictureMode()
    menu.itemconfig(label, text="Current Picture Mode: " + str(Picturemode))

def releaseCloseMenuButton(button, menu):
    button.configure(bg="white")
    menu.destroy()

def releasePowerButton(button):
    button.configure(bg="white")
    root.destroy()

def quit_program ():
    root.destroy()

def close_menu():
    button1.destroy()

def openMenu(event):
    # menu will be another canvas on top of the clockFrame canvas
    menuCanvas = Canvas(clockFrame, bg="white", width=w, height=600, highlightthickness=0)
    menuLabel = menuCanvas.create_text(512, 40, fill="black", justify="center", font="Arial 28", text="Menu")

    # style of pictures
    currentStyleLabel = menuCanvas.create_text(512, 100, fill="black", justify="center", font="Arial 16", text="Current Style: " + style)
    changeStyleButton = Canvas(menuCanvas, bg="white", width=250, height=30)
    changeStyleButtonLabel = changeStyleButton.create_text(125, 15, text="Change Style", font=("Arial", 16))
    changeStyleButton.bind("<ButtonPress-1>", lambda x: pressButton(changeStyleButton))
    changeStyleButton.bind("<ButtonRelease-1>", lambda x: releaseChangeStyleButton(changeStyleButton, currentStyleLabel, menuCanvas))

    # picture mode
    # TODO: will toggle modes such as..
    # BackgroundPics    = Pictures without Numbers overlaid with numbers (e.g. family pics)
    # NumberPics        = Pictures that already contain numbers (e.g. NBA jerseys)
    currentPictureModeLabel = menuCanvas.create_text(512, 250, fill="black", justify="center", font="Arial 16", text="Current Picture Mode: " + str(Picturemode))
    changePictureModeButton = Canvas(menuCanvas, bg="white", width=250, height=30)
    changePictureModeButtonLabel = changePictureModeButton.create_text(125, 15, text="Change Picture Mode", font=("Arial", 16))
    changePictureModeButton.bind("<ButtonPress-1>", lambda x: pressButton(changePictureModeButton))
    changePictureModeButton.bind("<ButtonRelease-1>", lambda x: releaseChangePictureModeButton(changePictureModeButton, currentPictureModeLabel, menuCanvas))

    # close menu
    closeMenuButton = Canvas(menuCanvas, bg="white", width=250, height=30)
    closeMenuButtonLabel = closeMenuButton.create_text(125, 15, text="Close Menu", font=("Arial", 16))
    closeMenuButton.bind("<ButtonPress-1>", lambda x: pressButton(closeMenuButton))
    closeMenuButton.bind("<ButtonRelease-1>", lambda x: releaseCloseMenuButton(closeMenuButton, menuCanvas))

    # power
    powerButton = Canvas(menuCanvas, bg="white", width=250, height=30)
    powerButtonLabel = powerButton.create_text(125, 15, text="Power Off", font=("Arial", 16))
    powerButton.bind("<ButtonPress-1>", lambda x: pressButton(powerButton))
    powerButton.bind("<ButtonRelease-1>", lambda x: releasePowerButton(powerButton))

    # place menu and buttons
    # TODO: change buttons from Canvases to rectangle objects? might make more sense
    menuCanvas.place(x = 0, y = 0)
    changeStyleButton.place(x = 512, y = 150, anchor="center")
    changePictureModeButton.place(x = 512, y = 300, anchor="center")
    closeMenuButton.place(x = 512, y = 450, anchor="center")
    powerButton.place(x = 512, y = 500, anchor="center")

    button1 = Button(menuCanvas, text = "Quit Program", command = quit_program)
    button2 = Button(menuCanvas, text="Close Menu", command=close_menu, width=100)
    button3 = Button(menuCanvas, text="Change Style", command=changeStyle, width=100)
    button1.pack(fill=BOTH, expand=1)
    button2.pack(fill=BOTH, expand=1)
    button3.pack(fill=BOTH, expand=1)

# bind screen press for menu open
canvas.bind("<ButtonPress-1>", openMenu)
########################### END MENU SYSTEM ###########################

canvas.pack(side = BOTTOM)

# run time function
clock()

# Driver code
get_Host_name_IP() #Function call 

# infinite running loop
root.mainloop() 