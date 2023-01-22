#necessary imports
import json
import subprocess
import time
import os
import webbrowser
import asyncio
import requests
import zipfile
import re

#files
import osu_refresher

#flask
from flask import Flask, jsonify, redirect, render_template, request, make_response


#start the tab
localhost_url = "http://127.0.0.1:90"
webbrowser.get()
webbrowser.open(f"{localhost_url}/get-cached-data", new=1, autoraise=True)


#flask set up
app = Flask(  # Create a flask app
  __name__,
  template_folder='templates', # Name of html file folder
  static_folder='static' # Name of directory for static files
)
app.config['SECRET_KEY'] = "hugandafortnite"

#variables
url = "http://gdcheerios.com"
user_data = {}

#functions
def rename(game):
  for file in os.listdir("installs"):
    found = bool(re.search(game, file))
    if found:
      if file[-4:] == ".jar":
        os.rename(f"installs/{file}", f"installs/{game}.jar")
      else:
        os.rename(f"installs/{file}", f"installs/{game}.exe")

def download(url, game_name):
  filename = url[url.rfind('/') + 1:]
  with requests.get(url) as req:
    with open(f"installs/{game_name}.zip", 'wb') as f:
      for chunk in req.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)

  #with zipfile.ZipFile(f"installs/{game_name}.zip", 'r') as zip_ref:
  #  zip_ref.extractall("installs/")
#
  #os.remove(f"installs/{game_name}.zip")

  rename(game_name)

def hide_element(element):
  element.grid_remove()

def has_game(game):
  for file in os.listdir("installs"):
    found = bool(re.search(game, file))
    if found:
      return True

  return False

#endpoints
@app.route("/get-cached-data")
def receive_cached_data():
  global url
  global user_data
  username = request.cookies.get('username')
  if username == None:
    return redirect(f"{localhost_url}/")
  else:
    resp = redirect(f"{localhost_url}/")
    url = request.cookies.get("url")
    user_data = requests.get(f"{url}/api/account/login/{request.cookies.get('username')}+{request.cookies.get('password')}").json()
    return resp


@app.route("/")
def home():
  return render_template(
    "index.html",
    userData = user_data,
    url = url,
    has_game = has_game
  )

@app.route("/login-page")
def login_page():
  return render_template(
    "login.html",
    warning = ""
  )

@app.route("/login", methods=["POST"])
def login():
  global user_data
  username = request.form.get('nm')
  password = request.form.get('pw')
  login_result = requests.get(f"{url}/api/account/login/{username}+{password}").json()
  print(login_result)
  if login_page == "incorrect info":
    resp = make_response(render_template(
        'login.html',
        warning = "incorrect info"
      ))
    return resp
  else:
    resp = make_response(redirect(f"{localhost_url}/"))
    resp.set_cookie("username", username)
    resp.set_cookie("password", password)
    user_data = login_result
    return resp

@app.route("/change-server")
def change_server():
  return render_template(
    "change-server.html",
    warning = ""
  )

@app.route("/submit-server-form", methods=["POST"])
def submit_server():
  global url
  ip = request.form.get('ip')
  port = request.form.get('port')
  if port != "":
      port = f":{port}"
  resp = make_response(redirect(f"{localhost_url}/"))
  try:
    request_result = requests.get(f"{ip}{port}")
    url = f"{ip}{port}"
    resp.set_cookie("url", url)
    return resp
  except:
    return render_template(
      "change-server.html",
      warning = f"Can't seem to find conection at {ip}{port}"
    )
    

@app.route("/signout")
def signout():
  resp = make_response(redirect(f"{localhost_url}/"))
  resp.delete_cookie("username")
  resp.delete_cookie("password")
  return resp

@app.route("/start_osu_refresher")
def start_osu_refresher():
  if osu_refresher.get_watch() != None:
    return redirect(f"{localhost_url}/")
  else:
    print(url)
    osu_refresher.prepare(user_data["metadata"]["osu id"], url)
    osu_refresher.credits()
    asyncio.run(osu_refresher.request_loop())
    return redirect(f"{localhost_url}/")

@app.route("/install/<game>")
def install(game):
  if game == "Gentry's Quest":
    req = requests.get("https://api.github.com/repos/gdcheeriosyt/Gentrys-Quest-Python/releases/latest").json()
    download(req["assets"][0]["browser_download_url"], "Gentry's Quest")

  return redirect(f"{localhost_url}")

@app.route("/uninstall/<game>")
def uninstall(game):
  try:
    os.remove(f"installs/{game}.jar")
  except FileNotFoundError:
    os.remove(f"installs/{game}.exe")


  return redirect(f"{localhost_url}")

@app.route("/verify/<game>")
def verify(game):
  rename(game)

  return redirect(f"{localhost_url}")

@app.route("/play/<game>+<username>+<password>")
def play(game, username, password):
  args = f" -u\"{username}\" -p\"{password}\""
  os.system(f"start \"poop\" \"installs/{game}\" {args}")

  return redirect(f"{localhost_url}")

@app.route("/end", methods=['POST'])
def end():
  print("bruh")
  sys.exit()

if __name__ == "__main__":
  app.run(
    host='0.0.0.0',
    port=90,
    debug=False)