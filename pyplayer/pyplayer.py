from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from os import listdir, environ
from pathlib import Path
from random import shuffle
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from pygame import mixer, mixer_music
from mutagen.mp3 import MP3


root = ttk.Window(themename="superhero")

TITLE = "Pyplayer"
SIZE = (40, 40)
BUTTON_STYLE = LINK

ICON_LEFT = ImageTk.PhotoImage(Image.open("./media/icon_left.png").resize(SIZE))
ICON_PLAY = ImageTk.PhotoImage(Image.open("./media/icon_play.png").resize(SIZE))
ICON_PAUSE = ImageTk.PhotoImage(Image.open("./media/icon_pause.png").resize(SIZE))
ICON_RIGHT = ImageTk.PhotoImage(Image.open("./media/icon_right.png").resize(SIZE))
PYGAME_LOGO = "./media/PYGAME_LOGO.ico"

mixer.init()

class Application:

    def __init__(self, root):
        
        songs = list()
        with open("./playlist", 'r') as f:
            for line in f:
                folder_path = Path(str(line).rstrip())
                backslash = '\\'
                songs += [f"{folder_path}{backslash}{file}" for file in listdir(folder_path) if not file.endswith(".spotdl-cache")]
        shuffle(songs)


        global paused
        global playing 
        global i
        global song_dur
        playing = False
        paused = False
        i = 0
        song_dur = 0.0

        def play_song():
            global playing
            global paused
            global i
            
            if playing and not paused:
                mixer_music.pause()
                paused = True
            elif not playing and paused:
                mixer_music.unpause()
                paused = False
            else:
                i+=1
                mixer_music.load(songs[i])
                mixer_music.play()
            
            playing = not playing
            button_play["image"] = ICON_PAUSE if playing else ICON_PLAY

            update_pos()
            update_song_dur()

        def previous_song():
            global i
            global playing
            i-=1

            pos.set(0)
            mixer_music.unload()
            mixer_music.load(songs[i])
            mixer_music.play()
            button_play["image"] = ICON_PAUSE
            update_song_dur()

        def next_song():
            global i
            global playing
            i+=1

            pos.set(0)
            mixer_music.unload()
            mixer_music.load(songs[i])
            mixer_music.play()
            button_play["image"] = ICON_PAUSE
            update_song_dur()

        def set_vol(var):
            mixer_music.set_volume(float(var))
        
        def set_pos(var):
            mixer_music.play(start=float(var))

        def update_song_dur():
            song_dur = get_mp3_length(songs[i])
            bottom_slider.config(to=song_dur)

        def update_pos():
            if paused: 
                root.after(1000, update_pos)
                return

            if not mixer_music.get_busy() and not paused:
                next_song()

            pos.set(min((pos.get() + 1.0), get_mp3_length(songs[i])))
            root.after(1000, update_pos)

        def get_mp3_length(filepath):
            try:
                audio = MP3(filepath)
                length_in_seconds = int(audio.info.length)
                return length_in_seconds
            except Exception as e:
                print(f"Error: {e}")
                return None

        ### BUTTON STYLE ###
        btn_style = ttk.Style()

        ### MAINFRAME ###
        root.title(TITLE)
        root.iconbitmap(PYGAME_LOGO)
        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0)

        ### BOTTOM FRAME ###
        bottom_frame = ttk.Frame(mainframe)
        bottom_frame.grid(column=0, columnspan=4, row=2)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        ### BOTTOM SLIDER ###
        pos = DoubleVar(); pos.set(0)
        bottom_slider = ttk.Scale(bottom_frame, orient=HORIZONTAL, variable=pos, command=set_pos, length=200, from_=0, to=1)
        bottom_slider.grid(column=1, columnspan=3, row=1, padx=10)

        ### VOLUME SLIDER ###
        vol = DoubleVar(); vol.set(mixer_music.get_volume())
        volume_slider = ttk.Scale(bottom_frame, orient=VERTICAL, variable=vol ,command=set_vol, length=50, from_=1, to=0)
        volume_slider.grid(column=4, row=1, padx=10)

        ### TOP FRAME ###
        top_frame = ttk.Frame(mainframe)
        top_frame.grid(column=0, columnspan=4,row=1)

        ### BUTTONS ###
        button_left = ttk.Button(top_frame, command=lambda: previous_song(), image=ICON_LEFT, bootstyle=BUTTON_STYLE)
        button_left.grid(column=1, row=1)
        button_play = ttk.Button(top_frame, command=lambda: play_song(), image=ICON_PLAY, bootstyle=BUTTON_STYLE)
        button_play.grid(column=2, row=1)
        button_right = ttk.Button(top_frame, command=lambda: next_song(), image=ICON_RIGHT, bootstyle=BUTTON_STYLE)
        button_right.grid(column=3, row=1)

Application(root)
root.mainloop()