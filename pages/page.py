import tkinter as tk
from tkinter import ttk
from event_emitter import EventEmitter

# =========================
# 页面类
# =========================
class Page(ttk.Frame, EventEmitter):
    def __init__(self, parent, page_id):
        ttk.Frame.__init__(self, parent)
        EventEmitter.__init__(self)
        self.page_id = page_id
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._create_widgets()
        self._bind_events()

    def create_widgets(self):
        pass

    def bind_events(self):
        pass

    def update(self):
        pass

    def _create_widgets(self):
        self.create_widgets()

    def _bind_events(self):
        self.on("processed", self._update)
        self.bind_events()

    def _update(self, result):
        self.update(result)