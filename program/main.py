import time
import os
import atexit
import requests
import psutil

url = "http://gdcheerios.com"
    
os.startfile(os.path.normpath("program/gosumemory.exe"))
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

atexit.register(exit_handler)

with open("id.txt", "r") as id_info:
  id = id_info.read()

print("https://github.com/l3lackShark/gosumemory")
print("I use this for data reading, so thanks to him")

time.sleep(5)
completed = False #boolean represents if map is completed or not

fail_iteration = 0 #check if something is going wrong, if something is then it will get bigger for the amount of times the error has occurred

while True:
  try:
    delay = float(requests.get(f"{url}]/api/get-delay").json())
  except:
    delay = 5
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
    
    if fail_iteration < 1:
      print('''
            something isn't right...
            the problem is most likely:
            1.osu! isn't open
            2.gdcheerios.com is offline''')
      requests.post(f"{url}/api/live/del/{id}")
      
    fail_iteration += 1