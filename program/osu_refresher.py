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


# states
'''
NotRunning = -1
MainMenu = 0
EditingMap = 1
Playing = 2
GameShutdownAnimation = 3
SongSelectEdit = 4
SongSelect = 5
WIP_NoIdeaWhatThisIs =6
ResultsScreen = 7
GameStartupAnimation = 10
MultiplayerRooms = 11
MultiplayerRoom = 12
MultiplayerSongSelect = 13
MultiplayerResultsscreen = 14
OsuDirect = 15
RankingTagCoop = 17
RankingTeam = 18
ProcessingBeatmaps = 19
Tourney = 22
'''

async def request_loop():
  global watch
  time.sleep(5)
  completed = False #boolean represents if map is completed or not
  while True:
    time.sleep(0.2)
    try:
      info = requests.get("http://127.0.0.1:24050/json").json()
      important_info = {}
      important_info["user"] = id
      important_info["mapInfo"] = {
        "background" : f"https://assets.ppy.sh/beatmaps/{info['menu']['bm']['set']}/covers/cover.jpg",
        "metadata" : info['menu']['bm']['metadata'],
        "stats" : info['menu']['bm']['stats'],
        "mods" : info['menu']['mods']["str"]
      }

      state = info['menu']['state']
      if state == -1:
        state = "NotRunning"
      elif state == 0:
        state = "MainMenu"
      elif state == 1:
        state = "Editing Map"
      elif state == 2:
        state = "Playing"
      elif state == 3:
        state = "GameShutdownAnimation"
      elif state == 4:
        state = "SongSelectEdit"
      elif state == 5:
        state = "SongSelect"
      elif state == 6:
        state = "WIP_NoIdeaWhatThisIs"
      elif state == 7:
        state = "ResultsScreen"
      elif state == 10:
        state = "GameStartupAnimation"
      elif state == 11:
        state = "MultiplayerRooms"
      elif state == 12:
        state = "MultiplayerRoom"
      elif state == 13:
        state = "MultiplayerSongSelect"
      elif state == 14:
        state = "MultiplayerResultsScreen"
      elif state == 15:
        state = "OsuDirect"
      elif state == 17:
        state = "RankingTagCoop"
      elif state == 18:
        state = "RankingTeam"
      elif state == 19:
        state = "ProcessingBeatmaps"
      elif state == 22:
        state = "Tourney"
      else:
        state = "Unknown"

      important_info["state"] = state

      important_info["gameplay"] = {
        "score" : info['gameplay']['score'],
        "accuracy" : info['gameplay']['accuracy'],
        "combo" : info['gameplay']['combo']['current'],
        "grade":info["gameplay"]["hits"]["grade"]["current"],
        "maxCombo" : info['gameplay']['combo']['max'],
        "pp" : info['gameplay']['pp']['current'],
        "hundred" : info['gameplay']['hits']['100'],
        "fifty" : info['gameplay']['hits']['50'],
        "misses" : info['gameplay']['hits']['0'],
        "health" : info['gameplay']['hp']['normal'],
        "leaderboardPosition" : info['gameplay']['leaderboard']['ourplayer']['position']
      }

      update(important_info)
      completed = False
    except Exception as e:
      requests.post(f"{url}/api/live/del/{id}")
      print(e)
      print('''
            something isn't right...
            the problem is most likely:
            1.osu! isn't open
            2.gdcheerios.com is offline''')

      for i in range(50):
        print("\n")

      time.sleep(1)
