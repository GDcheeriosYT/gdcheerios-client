import time
import os
import atexit
import requests
import psutil

id = 0
watch = None
url = "127.0.0.1"

def prepare(user_id, web_url=url):
  global watch
  global id
  global url
  id = user_id
  url = web_url
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
      requests.post(f"{url}/api/live/del/{id}")
      watch.kill()
      watch = None

  atexit.register(exit_handler)

def get_watch():
  return watch


def credits():
  print("https://github.com/l3lackShark/gosumemory")
  print("I use this for data reading, so thanks to him")

def request_loop():
  global watch
  time.sleep(5)
  completed = False #boolean represents if map is completed or not
  while True:
    delay = 1
    try:
      info = requests.get("http://127.0.0.1:24050/json").json()
      if info['menu']['state'] != 2 and info['menu']['state'] != 7:
        important_info = {}
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        requests.post(f"{url}/api/live/update/{id}", json=important_info)
        completed = False
        time.sleep(delay)
        
      elif info['menu']['state'] == 7:
        if completed == False:
          requests.get(f"{url}/refresh/{id}")
          important_info = {}
          important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
          important_info["state"] = info['menu']['state']
          important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
          requests.post(f"{url}/api/live/update/{id}", json=important_info)
          completed = True
        time.sleep(delay)
        
      else:
        important_info = {}
        important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
        important_info["state"] = info['menu']['state']
        important_info["gameplay"] = {"score" : info['gameplay']['score'], "accuracy" : info['gameplay']['accuracy'], "combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"], "maxCombo" : info['gameplay']['combo']['max'], "pp" : info['gameplay']['pp']['current'], "hundred" : info['gameplay']['hits']['100'], "fifty" : info['gameplay']['hits']['50'], "misses" : info['gameplay']['hits']['0']}
        requests.post(f"{url}/api/live/update/{id}", json=important_info)
        completed = False
        time.sleep(delay)
      fail_iteration = 0
      print(f"the delay is {delay} seconds")
    except:
      delay = 3
      time.sleep(delay)
      print('''
            something isn't right...
            the problem is most likely:
            1.osu! isn't open
            2.gdcheerios.com is offline''')
      requests.post(f"{url}/api/live/del/{id}")
      watch.kill()
      watch = None
      break
