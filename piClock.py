from tkinter import * 
from tkinter.ttk import *
from time import strftime 
from PIL import ImageTk, Image

# creating tkinter window 
root = Tk() 
root.overrideredirect(True) # for removing borders on window

frame = Frame(root)
frame.pack()

# create a canvas
canvas = Canvas(frame, bg="black", width=1520, height=350, highlightthickness=0)
canvas.pack(side = BOTTOM)

# get image corresponding to number
def getNumberImagePath(number):
	switcher = {
		"0": "C:/Users/alecm/Desktop/PiClock/fancy/0.jpg",
		"1": "C:/Users/alecm/Desktop/PiClock/fancy/1.jpg",
		"2": "C:/Users/alecm/Desktop/PiClock/fancy/2.jpg",
		"3": "C:/Users/alecm/Desktop/PiClock/fancy/3.jpg",
		"4": "C:/Users/alecm/Desktop/PiClock/fancy/4.jpg",
		"5": "C:/Users/alecm/Desktop/PiClock/fancy/5.jpg",
		"6": "C:/Users/alecm/Desktop/PiClock/fancy/6.jpg",
		"7": "C:/Users/alecm/Desktop/PiClock/fancy/7.jpg",
		"8": "C:/Users/alecm/Desktop/PiClock/fancy/8.jpg",
		"9": "C:/Users/alecm/Desktop/PiClock/fancy/9.jpg"
	}
	return switcher.get(number, "invalid image number")

# TODO: need to clean this up and comment it
def time(): 
	timeString = strftime("%I%M%S")
	print(timeString)

	canvas.image0 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[0])))
	canvas.create_image(0, 0, image=canvas.image0, anchor='nw')
	canvas.image1 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[1])))
	canvas.create_image(250, 0, image=canvas.image1, anchor='nw')
	canvas.image2 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[2])))
	canvas.create_image(520, 0, image=canvas.image2, anchor='nw')
	canvas.image3 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[3])))
	canvas.create_image(750, 0, image=canvas.image3, anchor='nw')
	canvas.image4 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[4])))
	canvas.create_image(1020, 0, image=canvas.image4, anchor='nw')
	canvas.image5 = ImageTk.PhotoImage(Image.open(getNumberImagePath(timeString[5])))
	canvas.create_image(1270, 0, image=canvas.image5, anchor='nw')

	canvas.after(1000, time)

# TODO: enable toggling of styles
def toggle():
	print("toggled")
	canvas.delete("all")

buttonBG = Button(text = "Switch", command = toggle)
buttonBG.pack( side = BOTTOM)

# run time function
time()
  
root.mainloop() # infinite running loop