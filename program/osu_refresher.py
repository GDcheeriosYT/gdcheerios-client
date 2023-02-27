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
upload_counter = 0

def prepare(user_id, web_url=url):
  global watch
  global id
  global url
  id = user_id
  url = web_url
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
  print("I use this for data reading, so thanks to him\n")

@socket.event
def update(data):
  global upload_counter
  print(f"{upload_counter}", end="\r")
  socket.emit("update client status", data)
  upload_counter += 1

def stop():
  requests.post(f"{url}/api/live/del/{id}")

async def request_loop():
  global watch
  time.sleep(5)
  completed = False #boolean represents if map is completed or not
  while True:
    time.sleep(0.2)
    try:
      info = requests.get("http://127.0.0.1:24050/json").json()
      important_info = {}
      if info['menu']['state'] != 2 and info['menu']['state'] != 7:
        important_info["user"] = id
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        update(important_info)
        completed = False
        
      elif info['menu']['state'] == 7:
        if completed == False:
          requests.get(f"{url}/refresh/{id}")
          important_info["user"] = id
          important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
          important_info["state"] = info['menu']['state']
          important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
          update(important_info)
          completed = True
        
      else:
        important_info["user"] = id
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        update(important_info)
        completed = False
      fail_iteration = 0
    except Exception as e:
      print(e)
      print('''
            something isn't right...
            the problem is most likely:
            1.osu! isn't open
            2.gdcheerios.com is offline''')
      stop()
      break

