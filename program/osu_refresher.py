import time
import os
import atexit
import requests
import psutil
import socketio
import json

id = 0
watch = None
url = "127.0.0.1"
socket = socketio.Client()

def prepare(user_id, web_url=url):
  global watch
  global id
  global url
  id = user_id
  url = "https://gdcheerios.com"
  socket.connect(f"{url}", wait_timeout=3)
  print(socket.connection_url)
  socket.emit("test", "ping")
  try:
    os.startfile(os.path.normpath("program/gosumemory.exe"))
  except:
    os.startfile(os.path.normpath("gosumemory.exe"))
  def get_pid():
    for proc in psutil.process_iter():
      if proc.name() == "gosumemory.exe":
        print(proc)
        print(proc.pid)
        return(proc.pid)
      
  watch = psutil.Process(get_pid())

  def exit_handler():
      global watch
      requests.post(f"{url}/api/live/del/{id}")
      watch.kill()
      watch = None

  atexit.register(exit_handler)

def get_watch():
  return watch


def credits():
  print("https://github.com/l3lackShark/gosumemory")
  print("I use this for data reading, so thanks to him")

@socket.event
def update(data):
  print(socket.socketio_path)
  socket.emit("update client status", data)

async def request_loop():
  global watch
  time.sleep(5)
  completed = False #boolean represents if map is completed or not
  while True:
    time.sleep(0.1)
    try:
      info = requests.get("http://127.0.0.1:24050/json").json()
      important_info = {}
      if info['menu']['state'] != 2 and info['menu']['state'] != 7:
        important_info["user"] = id
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        print("1: 1")
        update(important_info)
        print("1: 2")
        completed = False
        
      elif info['menu']['state'] == 7:
        if completed == False:
          requests.get(f"{url}/refresh/{id}")
          important_info["user"] = id
          important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
          important_info["state"] = info['menu']['state']
          important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
          print("7: 1")
          update(important_info)
          print("7: 2")
          completed = True
        
      else:
        important_info["user"] = id
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        print("2: 1")
        update(important_info)
        print("2: 2")
        completed = False
      fail_iteration = 0
    except Exception as e:
      print(e)
      print('''
            something isn't right...
            the problem is most likely:
            1.osu! isn't open
            2.gdcheerios.com is offline''')
      time.sleep(1)
      for i in range(100): 
        print("\n")

def stop():
  requests.post(f"{url}/api/live/del/{id}")
