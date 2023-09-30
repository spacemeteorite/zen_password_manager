from typing import Protocol

import pyperclip

from password_manager.utils import PwdGenerator


class Model(Protocol):
    ...


class View(Protocol):
    ...


class Presenter:

    def __init__(self, model: Model, view: View):
        self.model = model()
        self.view = view(self)

    def handle_generate_password(self, event=None):
        password_length = self.view.var_int_password_length.get()
        flag_allow_special_characters = self.view.var_bool_flag_allow_special_characters.get()

        password = PwdGenerator.generate_pwd(password_length, flag_allow_special_characters)
        self.view.var_string_password.set(password)
        self.view.button_generate_password['text'] = '已复制！再次点击将刷新密码'
        pyperclip.copy(password)

    def run(self):
        self.view.run()
