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
w = 1024 # width for the Tk root
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

# create frame within root window for organization
frame = Frame(root)
frame.pack()

# create a canvas
canvas = Canvas(frame, bg="black", width=2048, height=600, highlightthickness=0)

# keep track of if the clock is running or not
running = True

# default image path
Picturemode = 0 #Picture Types, 0 = Pictures without Numbers, 1 = Pictures with Numbers
BackgroundPath = "./images/backgrounds"
NumberPath = "./images/Numbers"

# create list of contents in imagepPath: dirnames = directories
f = []
for (dirpath, dirnames, filenames) in walk(BackgroundPath):
    f.extend(filenames)
    break    
# print(dirnames)

styleList = dirnames

# iterator for style list
styleCycle = cycle(styleList)

# default style to first one
style = next(styleCycle)

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
  

# get image corresponding to number
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

# clears canvas and refreshes the time and time images
def refreshTime():

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
    global running
    global timeCheck

# Check to see if a minute has elapsed, if so then change the Style
#    if timeCheck != strftime("%I%M"):
#        timeCheck = strftime("%I%M")
#        changeStyle()

# if running has been set to false, turn the clock off
    if not running:
        return

    refreshTime()

    canvas.after(5000, clock)


# enable changing of Picture Modes
def changePictureMode():
    global Picturemode
    # if running has been set to false, keep clock off
    if not running:
        return
    Picturemode += 1
    if Picturemode > 3: Picturemode = 0
    print ("PictureMode: " + str(Picturemode))
    refreshTime()

# enable changing of styles
def changeStyle():
    global style
    
    # if running has been set to false, keep clock off
    if not running:
        return
    style = next(styleCycle)
    refreshTime()

########################### MENU SYSTEM ###########################
# TODO: refactor these button actions

#The Mode button decides which mode is enabled
# BackgroundPics    = Pictures without Numbers overlaid with numbers (e.g. family pics)
# NumberPics        = Pictures that already contain numbers (e.g. NBA jerseys)
def pressChangePictureModeButton(button):
    print ("pressChangePictureModeButton")
    button.configure(bg="grey")

def releaseChangePictureModeButton(button, menu):
    button.configure(bg="white")
    changePictureMode()
#    self.canvas.update_idletasks

def pressChangeStyleButton(button):
    button.configure(bg="grey")

def releaseChangeStyleButton(button, menu):
    button.configure(bg="white")
    changeStyle()
    menu.destroy()

def pressCloseMenuButton(button):
    button.configure(bg="grey")

def releaseCloseMenuButton(button, menu):
    button.configure(bg="white")
    menu.destroy()

def pressPowerButton(button):
    button.configure(bg="grey")

def releasePowerButton(button):
    button.configure(bg="white")
    root.destroy()

def openMenu(event):
    global h
    global Picturemode

    menu = Canvas(frame, bg="white", width=w, height=600, highlightthickness=0)

    changePictureModeButton = Canvas(menu, bg="white", width=250, height=30)
    changePictureModeLabel = changePictureModeButton.create_text(125, 15, text="test " + str(Picturemode), font=("Arial", 14))
    print ("Menuing!")
    changePictureModeButton.bind("<ButtonPress-1>", lambda x: pressChangePictureModeButton(changePictureModeButton))
    changePictureModeButton.bind("<ButtonRelease-1>", lambda x: releaseChangePictureModeButton(changePictureModeButton, menu))

    changeStyleButton = Canvas(menu, bg="white", width=250, height=30)
    changeStyleLabel = changeStyleButton.create_text(125, 15, text="Change Style", font=("Arial", 16))
    changeStyleButton.bind("<ButtonPress-1>", lambda x: pressChangeStyleButton(changeStyleButton))
    changeStyleButton.bind("<ButtonRelease-1>", lambda x: releaseChangeStyleButton(changeStyleButton, menu))

    closeMenuButton = Canvas(menu, bg="white", width=250, height=30)
    closeMenuLabel = closeMenuButton.create_text(125, 15, text="Close Menu", font=("Arial", 16))
    closeMenuButton.bind("<ButtonPress-1>", lambda x: pressCloseMenuButton(closeMenuButton))
    closeMenuButton.bind("<ButtonRelease-1>", lambda x: releaseCloseMenuButton(closeMenuButton, menu))

    powerButton = Canvas(menu, bg="white", width=250, height=30)
    powerLabel = powerButton.create_text(125, 15, text="Power Off", font=("Arial", 16))
    powerButton.bind("<ButtonPress-1>", lambda x: pressPowerButton(powerButton))
    powerButton.bind("<ButtonRelease-1>", lambda x: releasePowerButton(powerButton))

    menu.place(x = 0, y = 0)
    changeStyleButton.place(x = 512, y = 100, anchor="center")
    changePictureModeButton.place(x=512, y=150, anchor="center")
    closeMenuButton.place(x = 512, y = 200, anchor="center")
    powerButton.place(x = 512, y = 250, anchor="center")

    menu.create_text(512,10, fill="darkblue", justify="center",font="Times 20 italic bold",
                     text="Click the bubbles that are multiples of two.")

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
# rotate clock style each minute    
