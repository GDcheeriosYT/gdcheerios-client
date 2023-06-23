#necessary imports
from ursina import *

#files
import osu_refresher
from Server import Server
from User import User
from WelcomeScreen import WelcomeScreen
import program_data

local_server = False

app = Ursina()


if local_server:
  program_data.server = Server("http", "127.0.0.1", "80")
else:
  program_data.server = Server()

# window setup
window.editor_ui.disable()
window.borderless = False

server_text = Text(
  f"currently connected to {program_data.server.domain}",
  origin=(0.5, 0.5),
  position=window.top_right,
  parent=camera.ui
)

welcome_screen = WelcomeScreen(program_data.server, program_data.user)

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


def change_server():
  return render_template(
    "change-server.html",
    warning = ""
  )

def signout():
  resp = make_response(redirect(f"{localhost_url}/"))
  resp.delete_cookie("username")
  resp.delete_cookie("password")
  return resp


def start_osu_refresher():
  if osu_refresher.get_watch() != None:
    return redirect(f"{localhost_url}/")
  else:
    print(url)
    osu_refresher.prepare(user_data["metadata"]["osu id"], url)
    osu_refresher.credits()
    asyncio.run(osu_refresher.request_loop())
    return redirect(f"{localhost_url}/")


def install(game):
  if game == "Gentry's Quest":
    req = requests.get("https://api.github.com/repos/gdcheeriosyt/Gentrys-Quest-Python/releases/latest").json()
    download(req["assets"][0]["browser_download_url"], "Gentry's Quest")

  return redirect(f"{localhost_url}")

def uninstall(game):
  try:
    os.remove(f"installs/{game}.jar")
  except FileNotFoundError:
    os.remove(f"installs/{game}.exe")


  return redirect(f"{localhost_url}")

def verify(game):
  rename(game)

  return redirect(f"{localhost_url}")

def play(game, username, password):
  args = f" -u\"{username}\" -p\"{password}\""
  os.system(f"start \"poop\" \"installs/{game}\" {args}")

  return redirect(f"{localhost_url}")


if __name__ == "__main__":
  app.run()