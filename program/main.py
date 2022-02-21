import time
import os
import atexit
import requests
import psutil
from tkinter import *
import osu_refresher
    
def get_pid(program_name):
  for proc in psutil.process_iter():
    if proc.name() == program_name:
      print(proc)
      print(proc.pid)
      return(proc.pid)
    

def start_osu_refresher():
  osu_refresher.prepare()
  osu_refresher.credits()
  osu_refresher.request_loop()



window = Tk()
app = window
#buttons

start_osu = Button(text="osu", command=start_osu_refresher)
start_osu.place(x=0, y=0)
  
window.title("gdcheerios.com client")
window.geometry("320x320")
window.mainloop()