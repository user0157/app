import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def after_decorator(func):
    def wrapper(self, error):
        self.after(0, lambda: func(self, error))
    return wrapper

def show_loading_popup(message="正在加载，请稍候...", timeout=5000):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_loading_popup") and self._loading_popup:
                self._loading_popup.destroy()

            popup = tk.Toplevel(self)
            popup.title("请稍候")
            popup.geometry("250x100")
            popup.resizable(False, False)
            popup.grab_set()
            popup.protocol("WM_DELETE_WINDOW", lambda: None)

            label = ttk.Label(popup, text=message, font=("微软雅黑", 12))
            label.place(relx=0.5, rely=0.5, anchor="center")

            self.update_idletasks()
            popup.update_idletasks()

            main_x = self.winfo_rootx()
            main_y = self.winfo_rooty()
            main_width = self.winfo_width()
            main_height = self.winfo_height()

            popup_width = popup.winfo_width()
            popup_height = popup.winfo_height()

            x = main_x + (main_width // 2) - (popup_width // 2)
            y = main_y + (main_height // 2) - (popup_height // 2)

            popup.geometry(f"+{x}+{y}")

            self._loading_popup = popup
            self.update_idletasks()

            def close_popup():
                if hasattr(self, "_loading_popup") and self._loading_popup:
                    self._loading_popup.destroy()
                    self._loading_popup = None

            popup.after(timeout, close_popup)

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def close_loading_popup(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            if hasattr(self, "_loading_popup") and self._loading_popup:
                self._loading_popup.destroy()
                self._loading_popup = None
    return wrapper
