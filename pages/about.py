import tkinter as tk
from tkinter import ttk
from pages.page import Page
import datetime
from config import APP_NAME, VERSION, AUTHOR

class AboutPage(Page):
    def create_widgets(self):
        current_year = datetime.datetime.now().year
        about_text = (
            f"程序名称: {APP_NAME}\n"
            f"版本: {VERSION}\n"
            f"作者: {AUTHOR}\n"
            f"版权: © {current_year} {AUTHOR} 保留所有权利。\n"
            "感谢使用本程序！"
        )

        self.label = ttk.Label(self, text=about_text, justify="center", anchor="center")
        self.label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)