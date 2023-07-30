from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image

root = ttk.Window(themename="superhero")



size=40
arrow_left = ImageTk.PhotoImage(Image.open("./media/arrow_left.png").resize((size,size)))
arrow_play = ImageTk.PhotoImage(Image.open("./media/arrow_play.png").resize((size,size)))
arrow_right = ImageTk.PhotoImage(Image.open("./media/arrow_right.png").resize((size,size)))

title = "Pyplayer"

### MAINFRAME ###
root.title(title)
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)

### BOTTOM FRAME ###
bottom_frame = ttk.Frame(mainframe)
bottom_frame.grid(column=0, columnspan=4, row=2)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.rowconfigure(0, weight=1)

### BOTTOM SLIDER ###
bottom_slider = ttk.Scale(bottom_frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0)
bottom_slider.grid(column=1, columnspan=3, row=1, padx=10)

### VOLUME SLIDER ###
volume_slider = ttk.Scale(bottom_frame, orient=VERTICAL, length=50, from_=1.0, to=100.0)
volume_slider.grid(column=4, row=1, padx=10)

### TOP FRAME ###
top_frame = ttk.Frame(mainframe)
top_frame.grid(column=0, columnspan=4,row=1)

### BUTTONS ###
style = LINK
button_left = ttk.Button(top_frame, image=arrow_left, bootstyle=style).grid(column=1, row=1)
button_play = ttk.Button(top_frame, image=arrow_play, bootstyle=style).grid(column=2, row=1)
button_right = ttk.Button(top_frame, image=arrow_right, bootstyle=style).grid(column=3, row=1)

root.mainloop()