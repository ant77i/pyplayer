from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from os import listdir
from pathlib import Path
from random import shuffle
import threading
import asyncio
import time
from pygame import mixer, mixer_music


root = ttk.Window(themename="superhero")

TITLE = "Pyplayer"
SIZE = 40
BUTTON_STYLE = LINK

icon_left = ImageTk.PhotoImage(Image.open("./media/icon_left.png").resize((SIZE,SIZE)))
icon_play = ImageTk.PhotoImage(Image.open("./media/icon_play.png").resize((SIZE,SIZE)))
icon_pause = ImageTk.PhotoImage(Image.open("./media/icon_pause.png").resize((SIZE,SIZE)))
icon_right = ImageTk.PhotoImage(Image.open("./media/icon_right.png").resize((SIZE,SIZE)))

mixer.init()

class Application:

    def __init__(self, root):
        
        global playing 
        playing = False

        songs = list()
        with open("playlist", 'r') as f:
            for line in f:
                folder_path = Path(str(line).rstrip())
                backslash = '\\'
                songs += [f"{folder_path}{backslash}{file}" for file in listdir(folder_path) if not file.endswith(".spotdl-cache")]
        shuffle(songs)

        def _asyncio_thread(async_loop):
            async_loop.run_until_complete(play_song())

        def do_tasks(async_loop):
            global playing
            global first_time
            playing = not playing
            button_play["image"] = icon_pause if playing else icon_play

            if first_time:
                first_time = False
                threading.Thread(target=_asyncio_thread, args=(async_loop,), daemon=True).start()

        global paused
        global first_time
        global i
        i=0
        first_time = True
        paused = False
        async def play_song():
            global i

            mixer_music.load(songs[i])
            mixer_music.play()
            i+=1
            


        if mixer_music.get_busy():
            mixer_music.pause()
            paused = True
        elif not mixer_music.get_busy() and paused:
            mixer_music.unpause()
            paused = False
        
            

        def previous_song(x):
            global i
            global playing
            i-=1
            #playing = not playing
            mixer_music.unload()
            mixer_music.load(songs[i])
            mixer_music.play()
            print(playing, i)
        def next_song(x):
            global i
            global playing
            i+=1
            #playing = not playing
            mixer_music.unload()
            mixer_music.load(songs[i])
            mixer_music.play()
            print(playing, i)

        
        async_loop = asyncio.get_event_loop()
        
        ### BUTTON STYLE ###
        btn_style = ttk.Style()

        ### MAINFRAME ###
        root.title(TITLE)
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
        button_left = ttk.Button(top_frame, command=lambda: root.event_generate("<<Previous>>"), image=icon_left, bootstyle=BUTTON_STYLE)
        button_left.grid(column=1, row=1)
        button_play = ttk.Button(top_frame, command=lambda: do_tasks(async_loop), image=icon_play, bootstyle=BUTTON_STYLE)
        button_play.grid(column=2, row=1)
        button_right = ttk.Button(top_frame, command=lambda: root.event_generate("<<Next>>"), bootstyle=BUTTON_STYLE)
        button_right.grid(column=3, row=1)

        root.bind("<<Previous>>", previous_song)
        root.bind("<<Next>>", next_song)


Application(root)
root.mainloop()