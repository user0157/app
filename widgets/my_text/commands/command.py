import tkinter as tk

# 命令基类
class Command:
    def __init__(self, widget):
        self.widget = widget
    def execute(self):
        pass