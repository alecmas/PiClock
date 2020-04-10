from tkinter import * 
from tkinter.ttk import *
from time import strftime 
from PIL import ImageTk, Image
from itertools import cycle
import time # TODO: clean up imports

# INSTRUCTIONS:
# press/click once to change style
# press/hold for 5 seconds to exit clock

# creating tkinter window 
root = Tk()
w = 2048 # width for the Tk root
h = 600 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = 0
y = 0

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# TODO: second window maybe?
#min_frame = Tk()
#min_frame.geometry('1040x600+1041+1')

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
imagePath = "/home/pi/PiClock/images/"

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
        imageList[i] = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[i])).resize(
            (341, 600), Image.ANTIALIAS)
       )        
        canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
        xPos += 341

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

# initialize variable to keep track of how long screen is pressed
pressedTime = 0

# starts timer for screen being pressed
def press(event):
    global pressedTime
    pressedTime = time.time()
    print ("pressed at " + str(pressedTime))

# ends timer for screen being pressed
def release(event):
    global pressedTime
    releaseTime = time.time()
    print ("released at " + str(releaseTime))
    if (releaseTime >= pressedTime and releaseTime < pressedTime + 1):
        changeStyle()
        
    if (releaseTime >= pressedTime + 5):
        print ("exiting clock")
        root.destroy()

# bind screen press events
canvas.bind("<ButtonPress-1>", press)
canvas.bind("<ButtonRelease-1>", release)
canvas.pack(side = BOTTOM)

# run time function
clock()
  
# infinite running loop
root.mainloop() 
