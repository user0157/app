import tkinter as tk
from tkinter import ttk, messagebox
from pages.page import Page

class HomePage(Page):
    def __init__(self, master=None, page_id=None):
        super().__init__(master, page_id)
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # Definindo o estilo comum para a label e o botão
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Microsoft YaHei", 16, "bold"))
        style.configure("Custom.TButton", font=("Microsoft YaHei", 12))

        # Aplicando o estilo à label
        self.label = ttk.Label(container, text="开始", style="Custom.TLabel")
        self.label.grid(row=0, column=0, pady=(0, 20))

        page_buttons = [
            ("打开匹配价格界面", "process"),
            ("库存管理界面", "inventory"),
            ("关于", "about")
        ]

        # Criando os botões e aplicando o estilo
        for idx, (button_text, page_type) in enumerate(page_buttons):
            button = ttk.Button(container, text=button_text, command=lambda type=page_type: self.open_page(type), style="Custom.TButton")
            button.grid(row=idx + 1, column=0, pady=10, sticky="ew")

        container.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def open_page(self, type):
        self.emit("open_page", type)
