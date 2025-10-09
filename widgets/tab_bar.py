"""
import tkinter as tk
from tkinter import ttk
from event_emitter import EventEmitter

# =========================
# TabBar 配置
# =========================
TAB_ACTIVE_BG = "#bbb"  # 激活标签的背景色
TAB_INACTIVE_BG = "#ddd"  # 非激活标签的背景色

class Tab(tk.Frame, EventEmitter):
    def __init__(self, parent, page_id):
        # 构造Tab标签
        tk.Frame.__init__(self, parent, bg=TAB_INACTIVE_BG, bd=1, highlightbackground="#888", highlightthickness=1, height=35)
        EventEmitter.__init__(self)
        self.pack_propagate(False)  # 防止自动调整大小
        self.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
        self.page_id = page_id

        self.button = tk.Button(
            self, text=f"{self.page_id}", relief=tk.FLAT, bd=0, highlightthickness=0,
            bg=TAB_INACTIVE_BG, anchor='w', command=self._on_select,
            activebackground=TAB_ACTIVE_BG, activeforeground="black"
        )
        self.button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.close_button = tk.Button(
            self, text="X", relief=tk.FLAT, bd=0, highlightthickness=0,
            bg=TAB_INACTIVE_BG, command=self._on_close,
            activebackground=TAB_ACTIVE_BG, activeforeground="black"
        )
        self.close_button.pack(side=tk.RIGHT, fill=tk.Y)

    def set_active(self, active=True):
        # 设置标签是否为激活状态
        bg_color = TAB_ACTIVE_BG if active else TAB_INACTIVE_BG
        self.config(bg=bg_color)
        self.button.config(bg=bg_color)
        self.close_button.config(bg=bg_color)

    def rename(self, new_name):
        # 更新标签名称
        self.button.config(text=new_name)

    def _on_select(self):
        # 选择标签时触发事件
        self.emit("tab/on_select", self)

    def _on_close(self):
        # 关闭标签时触发事件
        self.emit("tab/on_close", self)

class TabBar(tk.Frame, EventEmitter):
    def __init__(self, parent, max_tabs=10):
        tk.Frame.__init__(self, parent, bg=TAB_INACTIVE_BG)
        EventEmitter.__init__(self)

        self.max_tabs = max_tabs

        self.tab_buttons_frame = tk.Frame(self, bg=TAB_INACTIVE_BG)
        self.tab_buttons_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.add_button = tk.Button(
            self, text="+", font=('Microsoft YaHei', 12), command=self.add_tab,
            bg="#eee", relief=tk.FLAT
        )
        self.add_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.tabs = []
        self.active_tab = None
        self.page_count = 1

    def add_tab(self, page_type="home"):
        if self.max_tabs is not None and len(self.tabs) >= self.max_tabs:
            return

        page_id = self.page_count
        self.page_count += 1

        tab = Tab(
            parent=self.tab_buttons_frame,
            page_id=page_id,
        )
        tab.on("tab/on_select", self._select_tab)
        tab.on("tab/on_close", self._close_tab)
        self.tabs.append(tab)
        self.emit("tab_added", page_id, page_type)        
        self._select_tab(tab)
        #tab.rename(f"页面 {page_id}")

    def _select_tab(self, tab):
        if tab is None:
            self.emit("tab_selected", None)
            return

        # 选择一个Tab
        if self.active_tab and self.active_tab in self.tabs:
            self.active_tab.set_active(False)

        tab.set_active(True)
        self.active_tab = tab
        self.emit("tab_selected", tab.page_id)

    def _close_tab(self, tab):
        # 关闭一个Tab
        if self.active_tab == tab:
            index = self.tabs.index(tab)
            self.tabs.remove(tab)
            tab.destroy()

            if self.tabs:
                # 如果有其他Tab，选择下一个Tab
                if index < len(self.tabs):
                    next_tab = self.tabs[index]
                else:
                    next_tab = self.tabs[index - 1]

                self._select_tab(next_tab)
            else:
                self.active_tab = None
                self._select_tab(None)
        else:
            self.tabs.remove(tab)
            tab.destroy()

        self.emit("tab_closed", tab.page_id)

    def get_tab_by_page_id(self, page_id):
        # 根据页面ID获取Tab
        for tab in self.tabs:
            if tab.page_id == page_id:
                return tab
        return None
    
    def get_active_tab(self):
        return self.active_tab.page_id if self.active_tab else None
"""
import tkinter as tk
from tkinter import ttk
from event_emitter import EventEmitter

TAB_ACTIVE_BG = "#bbb"
TAB_INACTIVE_BG = "#ddd"

class Tab(tk.Frame, EventEmitter):
    def __init__(self, parent, page_id):
        tk.Frame.__init__(self, parent, bg=TAB_INACTIVE_BG, bd=1, highlightbackground="#888", highlightthickness=1, height=35)
        EventEmitter.__init__(self)
        self.pack_propagate(False)
        self.pack(side=tk.LEFT, padx=2, pady=2)
        self.page_id = page_id

        self.button = tk.Button(
            self, text=f"{self.page_id}", relief=tk.FLAT, bd=0, highlightthickness=0,
            bg=TAB_INACTIVE_BG, anchor='w', command=self._on_select,
            activebackground=TAB_ACTIVE_BG, activeforeground="black"
        )
        self.button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.close_button = tk.Button(
            self, text="X", relief=tk.FLAT, bd=0, highlightthickness=0,
            bg=TAB_INACTIVE_BG, command=self._on_close,
            activebackground=TAB_ACTIVE_BG, activeforeground="black"
        )
        self.close_button.pack(side=tk.RIGHT, fill=tk.Y)

    def set_active(self, active=True):
        bg_color = TAB_ACTIVE_BG if active else TAB_INACTIVE_BG
        self.config(bg=bg_color)
        self.button.config(bg=bg_color)
        self.close_button.config(bg=bg_color)

    def rename(self, new_name):
        self.button.config(text=new_name)

    def _on_select(self):
        self.emit("tab/on_select", self)

    def _on_close(self):
        self.emit("tab/on_close", self)

class TabBar(tk.Frame, EventEmitter):
    def __init__(self, parent, max_tabs=10):
        tk.Frame.__init__(self, parent, bg=TAB_INACTIVE_BG)
        EventEmitter.__init__(self)

        self.max_tabs = max_tabs

        # Frame do botão "+" com largura fixa
        self.add_button_frame = tk.Frame(self, width=40, bg=TAB_INACTIVE_BG)
        self.add_button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = tk.Button(
            self.add_button_frame, text="+", font=('Microsoft YaHei', 12),
            command=self.add_tab, bg="#eee", relief=tk.FLAT
        )
        self.add_button.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Frame para os tabs
        self.tab_buttons_frame = tk.Frame(self, bg=TAB_INACTIVE_BG)
        self.tab_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tab_buttons_frame.bind("<Configure>", lambda e: self._resize_tabs())

        self.tabs = []
        self.active_tab = None
        self.page_count = 1

    def add_tab(self, page_type="home"):
        if self.max_tabs is not None and len(self.tabs) >= self.max_tabs:
            return

        page_id = self.page_count
        self.page_count += 1

        tab = Tab(self.tab_buttons_frame, page_id=page_id)
        tab.on("tab/on_select", self._select_tab)
        tab.on("tab/on_close", self._close_tab)
        self.tabs.append(tab)
        self.emit("tab_added", page_id, page_type)
        self._select_tab(tab)

        self._resize_tabs()

    def _select_tab(self, tab):
        if tab is None:
            self.emit("tab_selected", None)
            return

        if self.active_tab and self.active_tab in self.tabs:
            self.active_tab.set_active(False)

        tab.set_active(True)
        self.active_tab = tab
        self.emit("tab_selected", tab.page_id)

    def _close_tab(self, tab):
        if self.active_tab == tab:
            index = self.tabs.index(tab)
            self.tabs.remove(tab)
            tab.destroy()

            if self.tabs:
                next_tab = self.tabs[index] if index < len(self.tabs) else self.tabs[index - 1]
                self._select_tab(next_tab)
            else:
                self.active_tab = None
                self._select_tab(None)
        else:
            self.tabs.remove(tab)
            tab.destroy()

        self._resize_tabs()
        self.emit("tab_closed", tab.page_id)

    def get_tab_by_page_id(self, page_id):
        for tab in self.tabs:
            if tab.page_id == page_id:
                return tab
        return None
    
    def get_active_tab(self):
        return self.active_tab.page_id if self.active_tab else None

    def _resize_tabs(self):
        self.after_idle(self._do_resize_tabs)

    def _do_resize_tabs(self):
        if not self.tabs:
            return

        total_width = self.tab_buttons_frame.winfo_width()
        if total_width <= 1:
            return

        tab_count = len(self.tabs)
        tab_width = max(80, min(200, total_width // tab_count - 4))

        for tab in self.tabs:
            tab.config(width=tab_width)