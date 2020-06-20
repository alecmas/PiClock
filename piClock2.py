from os import walk
# import numpy
import socket
from tkinter import *
# from tkinter.ttk import *
from time import strftime
from PIL import ImageTk, Image
from itertools import cycle
import time  # TODO: clean up imports
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

# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

w = ws  # width for the Tk root
h = hs  # height for the Tk root
DigitMaxSize = (round(w / 4, 0), round(h, 0))  # maximum size of a given digit


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
canvas = Canvas(clockFrame, bg="black", width=w, height=h, highlightthickness=0)


# default image path
Picturemode = 0  # Picture Types, 0 = Pictures with Numbers, 1 = Pictures without Numbers
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
def get_host_name_ip():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ", host_name)
        print("IP : ", host_ip)
        print("Screen Size: ", ws, ",", hs)
    except:
        print("Unable to get Hostname and IP")


# get image corresponding to number - This routine used for photos that already have numbers, e.g. NBA jerseys (Mode 1)
def getnumberpath(number):
    switcher = {}
    for i in range(10):
        switcher[str(i)] = NumberedPhotosPath + "/" + Numberedstyle + "/" + str(i) + ".jpg"
        img = Image.open(NumberedPhotosPath + "/" + Numberedstyle + "/" + str(i) + ".jpg")

    return switcher.get(number, "invalid image number")


# get image corresponding to number - This routine used to get numbers for photos without numbers, e.g. Family Pics (Mode 0)
def getnumberimagepath(number):
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
    for (dirpath, dirnames, filenames) in walk(BackgroundPath + "/" + style):
        f.extend(filenames)
        break
        # print(filenames)
    # print(len(filenames))

    for i in range(10):
        switcher[str(i)] = BackgroundPath + "/" + style + "/" + filenames[randint(0, len(filenames) - 1)]

    return switcher.get(number, "invalid image number")


def refreshmode0time():
    canvas.delete("all")
    timeString = strftime("%I%M%S")

    xPos = 0
    for i in range(4):
        imageList[i] = Image.open(getnumberpath(timeString[i]))
        imageList[i].thumbnail(DigitMaxSize)
        imageList[i] = ImageTk.PhotoImage(imageList[i])
        canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
        xPos += round(w / 4, 0)


# clears canvas and refreshes the time and time images
def refreshmode1time():
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
        imageList[i] = (Image.open(getnumberimagepath(timeString[i])))
        imwidth, imheight = imageList[i].size
        # Paste the foreground onto the BackgroundImageList
        BackgroundImage.paste(imageList[i], (int(bwidth / 2 - imwidth / 2), bheight - imheight - 10), imageList[i])
        junk[i] = ImageTk.PhotoImage(BackgroundImage)
        # canvas.create_image(xPos, 0, image=junk, anchor='nw')
        canvas.create_image(xPos, h, image=junk[i], anchor='sw')
        xPos += round(w / 4, 0)
        # print ("xPos:",xPos)


# main clock function loop which refreshes every 1 sec
def clock():
    global timeCheck
    if Picturemode == 0:
        refreshmode0time()
    else:
        refreshmode1time()
    canvas.after(5000, clock)


# enable changing of Picture Modes
def changepicturemode():
    global Picturemode
    Picturemode += 1
    if Picturemode > 1: Picturemode = 0
    if Picturemode == 0:
        refreshmode0time()
    else:
        refreshmode1time()

# enable changing of styles
def changeStyle():
    global style
    global Numberedstyle
    style = next(styleCycle)
    Numberedstyle = next(NumberedstyleCycle)

    if Picturemode == 0:
        refreshmode0time()
    else:
        refreshmode1time()
    openMenu

########################### MENU SYSTEM ###########################

def quit_program():
    root.destroy()
    sys.exit()

def close_menu(foo):
#     list = root.slaves()
#     print ("list: ",list)
#     print("Canvas: ",canvas.gettags(item))
#     print("canvas findall: ",canvas.find_all())
#     print("menuCanvas findall: ", menuCanvas.find_all())
     foo.destroy()

#    for l in list:
#        l.destroy()


def openMenu(event):
    # menu will be another canvas on top of the clockFrame canvas
#    menuCanvas = Canvas(clockFrame, bg="white", width=w, height=int(1200), highlightthickness=0)
    menuCanvas = Tk()
    menuCanvas.title('Test Title')
    menuCanvas.geometry(str(int(ws/2))+"x"+str(int(hs/2))+"+0+0")

#    menuLabel = menuCanvas.create_text(512, 40, fill="black", justify="center", font="Arial 28", text="Menu")

    # picture mode
    # TODO: will toggle modes such as..
    # BackgroundPics    = Pictures without Numbers overlaid with numbers (e.g. family pics)
    # NumberPics        = Pictures that already contain numbers (e.g. NBA jerseys)

    # place menu and buttons
    # TODO: change buttons from Canvases to rectangle objects? might make more sense
 #   menuCanvas.grid(x=0, y=0)
#    menuCanvas.place(x=0, y=0, width=ws/2, height=hs/2)
    Grid.rowconfigure(menuCanvas, 0, weight=1)
    Grid.rowconfigure(menuCanvas, 1, weight=1)
    Grid.rowconfigure(menuCanvas, 2, weight=1)
    Grid.columnconfigure(menuCanvas, 0, weight=1)
    Grid.columnconfigure(menuCanvas, 1, weight=1)

    button1 = Button(menuCanvas, text="Quit Program", command=quit_program)
    button2 = Button(menuCanvas, text="Close Menu", command=lambda: close_menu(menuCanvas))
    button3 = Button(menuCanvas, text="Change Style: "+Numberedstyle, command=changeStyle)
    button4 = Button(menuCanvas, text="Change Photo Mode " + str(int(Picturemode)), command=changepicturemode)
    button5 = Button(menuCanvas, text="Screen Size: "+str(ws)+","+str(hs))
    button6 = Button(menuCanvas, text="Max Digit: "+str(int(DigitMaxSize[0]))+","+str(int(DigitMaxSize[1])))
    button1.grid(row=0, column=0, sticky="NSEW")
    button2.grid(row=0, column=1, sticky="NSEW")
    button3.grid(row=1, column=0, sticky="NSEW")
    button4.grid(row=1, column=1, sticky="NSEW")
    button5.grid(row=2, column=0, sticky="NSEW")
    button6.grid(row=2, column=1, sticky="NSEW")
#    button1.pack(side="top", fill=X)
#    button2.pack(side="top", fill=X)
#    button3.pack(side="top", fill=X)
#    button4.pack(side="top", fill=X)
# bind screen press for menu open
canvas.bind("<ButtonPress-1>", openMenu)
########################### END MENU SYSTEM ###########################

canvas.pack(side=BOTTOM)

# run time function
clock()

# Driver code
get_host_name_ip()  # Function call

# infinite running loop
root.mainloop()
#while True:
#    root.update_idletasks()
#    root.update()
