from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path

arrow_next = ImageTk.PhotoImage(Image.open("./media/arrow_next.png"))
arrow_play = ImageTk.PhotoImage(Image.open("./media/arrow_play.png"))
arrow_previous = ImageTk.PhotoImage(Image.open("./media/arrow_previous.png"))
title = "Pyplayer"

root = Tk()

### MAINFRAME ###
root.title(title)
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)

### BOTTOM SLIDER ###
bottom_slider = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=1.0, to=100.0)
bottom_slider.grid(column=1, columnspan=3, row=2)

### VOLUME SLIDER ###
volume_slider = ttk.Scale(mainframe, orient=VERTICAL, length=50, from_=1.0, to=100.0)
volume_slider.grid(column=4, row=2)

### TOP FRAME ###
top_frame = ttk.Frame(mainframe)
top_frame.grid(column=1, columnspan=3, row=1)

### BUTTONS ### 
button_play = ttk.Button(top_frame, image=arrow_play).grid(column=2, row=1)
button_previous = ttk.Button(top_frame, image=arrow_previous).grid(column=1, row=1)
button_next = ttk.Button(top_frame, image=arrow_next).grid(column=3, row=1)

root.mainloop()