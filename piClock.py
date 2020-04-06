from tkinter import * 
from tkinter.ttk import *
from time import strftime 
from PIL import ImageTk, Image
from itertools import cycle

# creating tkinter window 
root = Tk() 
root.overrideredirect(True) # for removing borders on window

# create frame within root window for organization
frame = Frame(root)
frame.pack()

# create a canvas
canvas = Canvas(frame, bg="black", width=1500, height=350, highlightthickness=0)
canvas.pack(side = BOTTOM)

# keep track of if the clock is running or not
running = True

# list of all possible styles
styleList = ["fancy",
			"nba"]

# iterator for style list
styleCycle = cycle(styleList)

# default style to first one
style = next(styleCycle)

# initialize images to default style
canvas.image0 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))
canvas.image1 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))
canvas.image2 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))
canvas.image3 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))
canvas.image4 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))
canvas.image5 = ImageTk.PhotoImage(Image.open("C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg"))

# put images in list for easier modification later
imageList = [canvas.image0,
			canvas.image1,
			canvas.image2,
			canvas.image3,
			canvas.image4,
			canvas.image5]

# get image corresponding to number
def getNumberImagePath(number):
	switcher = {
		"0": "C:/Users/alecm/Desktop/PiClock/" + style + "/0.jpg",
		"1": "C:/Users/alecm/Desktop/PiClock/" + style + "/1.jpg",
		"2": "C:/Users/alecm/Desktop/PiClock/" + style + "/2.jpg",
		"3": "C:/Users/alecm/Desktop/PiClock/" + style + "/3.jpg",
		"4": "C:/Users/alecm/Desktop/PiClock/" + style + "/4.jpg",
		"5": "C:/Users/alecm/Desktop/PiClock/" + style + "/5.jpg",
		"6": "C:/Users/alecm/Desktop/PiClock/" + style + "/6.jpg",
		"7": "C:/Users/alecm/Desktop/PiClock/" + style + "/7.jpg",
		"8": "C:/Users/alecm/Desktop/PiClock/" + style + "/8.jpg",
		"9": "C:/Users/alecm/Desktop/PiClock/" + style + "/9.jpg"
	}

	return switcher.get(number, "invalid image number")

# clears canvas and refreshes the time and time images
def refreshTime():
	canvas.delete("all")
	timeString = strftime("%I%M%S")
	xPos = 0
	for i in range(6):
		imageList[i] = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[i])))
		canvas.create_image(xPos, 0, image=imageList[i], anchor='nw')
		xPos += 250

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

buttonPower = Button(text = "On/Off", command = power)
buttonPower.pack(side = BOTTOM)

buttonChangeStyle = Button(text = "Change Style", command = changeStyle)
buttonChangeStyle.pack(side = BOTTOM)

# run time function
clock()
  
root.mainloop() # infinite running loop