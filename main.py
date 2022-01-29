import time
import requests
import os
import atexit

def exit_handler():
    requests.post(f"http://gdcheerios.com/api/live/del/{id}")

atexit.register(exit_handler)

delay = 2

score = [0]
combo = [0]
accuracy = [0]

with open("id.txt", "r") as f:
  id = f.read()

print("https://github.com/l3lackShark/gosumemory")
print("I use this for data reading, so thanks to him")

os.startfile("gosumemory.exe")

time.sleep(5)
completed = False #boolean represents if map is completed or not

while True:
  print(score[len(score)-1])
  print(combo[len(combo)-1])
  print(accuracy[len(accuracy)-1])
  info = requests.get("http://127.0.0.1:24050/json").json()
  if info['menu']['state'] != 2 and info['menu']['state'] != 7:
    important_info = {}
    important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
    important_info["state"] = info['menu']['state']
    important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
    score.append(info['gameplay']['score'])
    combo.append(info['gameplay']['combo']['current'])
    accuracy.append(info['gameplay']['accuracy'])
    important_info["lists"] = {"combo" : combo, "accuracy" : accuracy, "score" : score}
    requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
    completed = False
    time.sleep(delay)
    score = [0]
    combo = [0]
    accuracy = [0]
    
  elif info['menu']['state'] == 7:
    if completed == False:
      requests.get(f"http://gdcheerios.com/refresh/{id}")
      important_info = {}
      important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
      important_info["state"] = info['menu']['state']
      important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
      score.append(info['gameplay']['score'])
      combo.append(info['gameplay']['combo']['current'])
      accuracy.append(info['gameplay']['accuracy'])
      important_info["lists"] = {"combo" : combo, "accuracy" : accuracy, "score" : score}
      requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
      completed = True
    time.sleep(delay)
    score = [0]
    combo = [0]
    accuracy = [0]
    
  else:
    important_info = {}
    important_info["mapInfo"] = {"background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg","metadata" : info['menu']['bm']['metadata'],"stats" : info['menu']['bm']['stats'],"mods" : info['menu']['mods']["str"]}
    important_info["state"] = info['menu']['state']
    important_info["gameplay"] = {"score" : info['gameplay']['score'],"accuracy" : info['gameplay']['accuracy'],"combo" : info['gameplay']['combo']['current'], "grade":info["gameplay"]["hits"]["grade"]["current"]}
    score.append(info['gameplay']['score'])
    combo.append(info['gameplay']['combo']['current'])
    accuracy.append(info['gameplay']['accuracy'])
    important_info["lists"] = {"combo" : combo, "accuracy" : accuracy, "score" : score}
    requests.post(f"http://gdcheerios.com/api/live/update/{id}", json=important_info)
    completed = False
    time.sleep(delay)
