import tkinter as tk
from tkinter import ttk, messagebox
from pages.page import Page

class MainPage(Page):
    def __init__(self, master=None, page_id=None):
        super().__init__(master, page_id)
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 16))

        self.label = ttk.Label(container, text="Escolha a página:")
        self.label.grid(row=0, column=0, pady=(0, 20))

        page_buttons = [
            "Página 1",
            "Página 2",
            "Página 3",
        ]

        for idx, page_name in enumerate(page_buttons):
            button = ttk.Button(container, text=page_name, command=lambda pid=page_name: self.open_page(pid))
            button.grid(row=idx + 1, column=0, pady=10, sticky="ew")

        container.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def open_page(self, page_id):
        messagebox.showinfo("Navegação", f"Navegando para {page_id}")
