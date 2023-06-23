from ursina import *
from ursina.prefabs.input_field import InputField


class LoginBox(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(
            model="quad",
            origin=(0, 0),
            color=rgb(117, 117, 117, 0),
            *args,
            **kwargs
        )

        self.username_box = InputField("Username", position=(0, 0.2), parent=self)
        self.password_box = InputField("Password", position=(0, -0.1), hide_content=True, parent=self)
        self.login_status = Text("", position=(0, 0.28), origin=(0, 0), scale=(3, 3.2), parent=self)
        self.submit_button = Button("Submit", position=(0, -0.4), scale=(0.2, 0.15), parent=self)
