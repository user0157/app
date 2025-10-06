import tkinter as tk
from tkinter import ttk
from pages.page import Page

class ComingSoon(Page):
    def __init__(self, parent, page_id):
        super().__init__(parent, page_id)
        
    def create_widgets(self):
        self.message_label = ttk.Label(self, text="此功能尚未实现", font=("Arial", 20, "bold"))
        self.message_label.grid(row=0, column=0, padx=10, pady=10)