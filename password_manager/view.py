from typing import Protocol

import pathlib

import tkinter as tk
from tkinter import ttk, messagebox

from screeninfo import get_monitors


class Presenter(Protocol):
    def handle_generate_password(self, event: tk.Event=None) -> None:
        ...


class View(tk.Tk):

    def __init__(self, presenter: Presenter):
        super().__init__()

        self.presenter = presenter

        # get user screen info
        self.SCREEN_WIDTH = int()
        self.SCREEN_HEIGHT = int()
        self.RATIO = int()

        # get static file path
        self.ROOT_PATH = pathlib.Path(__file__).parent.parent.resolve()
        self.STATIC_PATH = self.ROOT_PATH / 'static'


    def set_window_ratio(self):
        """根据屏幕分辨率调节软件大小"""
        for m in get_monitors(): # 根据屏幕分辨率改变界面大小
            if m.is_primary:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (m.width, m.height)
                self.RATIO = round(self.SCREEN_HEIGHT / 1080) # 为避免带鱼屏，所以不适用横向分辨率，而使用纵向分辨率
                print(f"primary screen size: ({self.SCREEN_WIDTH}, {self.SCREEN_HEIGHT})\nresizing ratio: {self.RATIO}")


    def window_init(self):
        print('初始化窗口中')

        # window variables
        self.variables = dict()

        # window metadata
        self.title(" ZEN 密码管理器")

        self.iconbitmap(self.STATIC_PATH / 'key.ico')
        self.resizable(False, False)

        # 设置窗口大小以及位置（默认居中）
        window_width = 300 * self.RATIO
        window_height = 150 * self.RATIO
        left_position = round((self.SCREEN_WIDTH - window_width) / 2)
        top_position = round((self.SCREEN_HEIGHT - window_height) / 2)
        print(f"窗口宽度: {window_width} | 窗口高度: {window_height} | 缩放比例: {self.RATIO} | 窗口位置: 居中")
        self.geometry(f"{window_width}x{window_height}+{left_position}+{top_position}")


    def variable_init(self):
        self.var_string_password = tk.StringVar()
        self.var_int_password_length = tk.IntVar()
        self.var_bool_flag_allow_special_characters = tk.BooleanVar()


    def widgets_init(self):
        print('初始化控件')

        # widgets creation
        self.frame_main = tk.Frame(self)
        self.button_generate_password = ttk.Button(self.frame_main, text='生成密码')
        self.label_password = tk.Label(self.frame_main,
                                       textvariable=self.var_string_password,
                                       relief='solid',
                                       bg='black')

        self.frame_options = tk.Frame(self.frame_main)
        self.spinbox_password_length = ttk.Spinbox(self.frame_options,
                                                   textvariable=self.var_int_password_length,
                                                   from_=1,
                                                   to=999,
                                                   increment=1)
        self.var_int_password_length.set(10)
        self.checkbox_allow_special_characters = tk.Checkbutton(self.frame_options, text='使用特殊字符',
                                                                variable=self.var_bool_flag_allow_special_characters)

    def widgets_layout(self):
        print('控件布局中')
        # widgets grid layout
        self.columnconfigure(0, weight=1)

        self.frame_main.grid(row=0, column=0, sticky='we')
        self.frame_main.columnconfigure(0, weight=1)

        self.button_generate_password.grid(row=0, column=0, sticky='we')
        self.label_password.grid(row=1, column=0, sticky='we')
        self.frame_options.grid(row=2, column=0, sticky='we')

        self.spinbox_password_length.grid(row=0, column=0, sticky='we')
        self.checkbox_allow_special_characters.grid(row=0, column=1, sticky='we', padx=10)

        for child in self.frame_main.winfo_children():
            child.grid(padx=15*self.RATIO, pady=8*self.RATIO)


    def widgets_bind_events(self):
        print('绑定事件中')
        # widgets event bindings
        self.button_generate_password.bind('<ButtonRelease-1>', self.presenter.handle_generate_password)
        self.label_password.bind('<Enter>', self.handle_enter_label_password)
        self.label_password.bind('<Leave>', self.handle_leave_label_password)

    def handle_enter_label_password(self, event=None):
        self.label_password.configure(bg='white')

    def handle_leave_label_password(self, event=None):
        self.label_password.configure(bg='black')

    def msgbox_info(self, title: str, info: str) -> None:
        messagebox.showinfo(title, info)

    def msgbox_error(self, title: str, error: str) -> None:
        messagebox.showerror(title, error)

    def msgbox_warning(self, title: str, warning: str) -> None:
        messagebox.showwarning(title, warning)

    def run(self) -> None:
        self.set_window_ratio()
        self.window_init()
        self.variable_init()
        self.widgets_init()
        self.widgets_layout()
        self.widgets_bind_events()
        self.mainloop()


if __name__ == "__main__":
    app = View()
    app.run()
