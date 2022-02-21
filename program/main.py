import time
import os
import atexit
from turtle import width
from tkinter import *
import osu_refresher


window = Tk()
app = window

#functions
def start_osu_refresher():
  osu_refresher.prepare()
  osu_refresher.credits() 
  osu_refresher.request_loop()

def start_stream_overlay():
  print("Coming Soon...")

#buttons
start_osu = Button(text="osu", command=start_osu_refresher)
start_osu.place(x=0, y=0)
start_overlay = Button(text="stream overlay", command=start_stream_overlay)
start_overlay.place(x=100, y=0)
  
window.title("gdcheerios.com client")
window.geometry("320x320")
window.mainloop()