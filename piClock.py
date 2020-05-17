from tkinter import * 
from tkinter.ttk import *
from time import strftime 
from PIL import ImageTk, Image
from itertools import cycle
import time # TODO: clean up imports

# INSTRUCTIONS:
# click on screen to open menu

# creating tkinter window
root = Tk()
w = 2048 # width for the Tk root
h = 600 # height for the Tk root

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
imagePath = "./images/"

# list of all possible styles
styleList = ["fancy",
            "nba"]

# iterator for style list
styleCycle = cycle(styleList)

# default style to first one
style = next(styleCycle)

# initialize images to default style
canvas.image0 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))
canvas.image1 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))
canvas.image2 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))
canvas.image3 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))
canvas.image4 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))
canvas.image5 = ImageTk.PhotoImage(Image.open(imagePath + style + "/0.jpg"))

# put images in list for easier modification later
imageList = [canvas.image0,
            canvas.image1,
            canvas.image2,
            canvas.image3,
            canvas.image4,
            canvas.image5]

# get image corresponding to number
def getNumberImagePath(number):
    switcher = {}
    
    for i in range(10):
        switcher[str(i)] = imagePath + style + "/" + str(i) + ".jpg"

    return switcher.get(number, "invalid image number")

# clears canvas and refreshes the time and time images
def refreshTime():
    canvas.delete("all")
    timeString = strftime("%I%M%S")
   
    xPos = 0
    for i in range(4):
        imageList[i] = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[i])))       
        canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
        xPos += 512

# main clock function loop which refreshes every 1 sec
def clock(): 
    global running

	# if running has been set to false, turn the clock off
    if not running:
        return

    refreshTime()

    canvas.after(1000, clock)

# enable changing of styles
def changeStyle():
    global style
    
    # if running has been set to false, keep clock off
    if not running:
        return

    style = next(styleCycle)

    refreshTime()

# toggles clock on or off
def power():
    global running

    if running:
        canvas.delete("all")
        running = False
    else:
        running = True

    clock()

########################### MENU SYSTEM ###########################
# TODO: refactor these button actions
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
    menu = Canvas(frame, bg="white", width=2048, height=600, highlightthickness=0)

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
    changeStyleButton.place(x = 512, y = 50)
    closeMenuButton.place(x = 512, y = 100)
    powerButton.place(x = 512, y = 150)

# bind screen press for menu open
canvas.bind("<ButtonPress-1>", openMenu)
########################### END MENU SYSTEM ###########################

canvas.pack(side = BOTTOM)

# run time function
clock()
  
# infinite running loop
root.mainloop()