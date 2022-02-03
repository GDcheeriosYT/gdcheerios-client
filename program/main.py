import time
import os
import atexit

def exit_handler():
    requests.post(f"http://gdcheerios.com/api/live/del/{id}")

try:
    import requests
except:
    install("requests")

atexit.register(exit_handler)

with open("id.txt", "r") as id_info:
  id = id_info.read()

print("https://github.com/l3lackShark/gosumemory")
print("I use this for data reading, so thanks to him")

os.startfile("gosumemory.exe")

time.sleep(5)
completed = False #boolean represents if map is completed or not

while True:
  delay = float(requests.get("http://gdcheerios.com/api/get-delay").json())
  info = requests.get("http://127.0.0.1:24050/json").json()
  if info['menu']['state'] != 2 and info['menu']['state'] != 7:
    important_info = {}
    important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
    important_info["state"] = info['menu']['state']
    important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
    requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
    completed = False
    time.sleep(delay)
    
  elif info['menu']['state'] == 7:
    if completed == False:
      requests.get(f"http://gdcheerios.com/refresh/{id}")
      important_info = {}
      important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
      important_info["state"] = info['menu']['state']
      important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
      requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
      completed = True
    time.sleep(delay)
    
  else:
    important_info = {}
    important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
    important_info["state"] = info['menu']['state']
    important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
    requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
    completed = False
    time.sleep(delay)
