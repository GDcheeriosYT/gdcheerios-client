from ursina import *
from LoginBox import LoginBox
import requests
import json
import program_data
from User import User


class WelcomeScreen(Entity):
    def __init__(self, server, user):
        super().__init__(parent=camera.ui)
        self.server = server
        self.user = user
        self.text_1 = Text(
            "Hello!",
            origin=(0, 0),
            position=(0, 0.3),
            parent=self
        )
        self.text_2 = Text(
            "It seems you are not logged in...",
            origin=(0, 0),
            position=(0, 0.25),
            parent=self
        )
        self.text_3 = Text(
            "Unfortunately it is required that you are logged in to use this client.",
            origin=(0, 0),
            position=(0, 0.2),
            parent=self
        )
        self.login_box = LoginBox(
            position=(-0.3, 0),
            scale=(0.5, 0.7),
            parent=self
        )
        self.login_box.submit_button.on_click = self.login

    def login(self):
        try:
            data = requests.get(f"{self.server.url}/api/account/login/{self.login_box.username_box.text}+{self.login_box.password_box.text}").json()
            program_data.user = User(self.login_box.username_box.text)
            program_data.user.id = data['id']
        except json.JSONDecodeError:
            pass
