import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from event_emitter import EventEmitter
from widgets.tab_bar import TabBar
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.about import AboutPage
from config import APP_NAME, VERSION
from app_decorators import after_decorator, show_loading_popup, close_loading_popup

# =========================
# 主应用类
# =========================
class App(tk.Tk, EventEmitter):
    def __init__(self):
        tk.Tk.__init__(self)
        EventEmitter.__init__(self)
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("900x600")
        self.logged_in = False

        self.pages = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.page_container = ttk.Frame(self)
        self.page_container.grid(row=1, column=0, sticky="nsew")
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(0, weight=1)

        self.tab_bar = TabBar(self)
        self.tab_bar.grid(row=0, column=0, sticky="ew")
        self.tab_bar.on("tab_added", self.create_new_page)
        self.tab_bar.on("tab_selected", self.show_page)
        self.tab_bar.add_tab()

        self.footer = tk.Frame(self, relief="raised", bd=1, bg="#f0f0f0")
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.footer.columnconfigure(0, weight=1)
        self.footer.columnconfigure(1, weight=1)
        self.footer.columnconfigure(2, weight=1)

        self.label_id = tk.Label(self.footer, text="", anchor="w", bg="#f0f0f0")
        self.label_id.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.label_role = tk.Label(self.footer, text="", anchor="center", bg="#f0f0f0")
        self.label_role.grid(row=0, column=1, sticky="n", pady=5)

        self.label_email = tk.Label(self.footer, text="", anchor="e", bg="#f0f0f0")
        self.label_email.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        self.reset_footer()

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="退出", command=self.logout)
        menu_bar.add_cascade(label="开始", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        
        self.config(menu=menu_bar)

    def show_about(self):
        self.tab_bar.add_tab("about")

    def create_new_page(self, page_id, page_type):
        if not self.logged_in and page_type != "login":
            page = LoginPage(self.page_container, page_id)
            page.on("page/login", self._emit_login)

        elif page_type == "about":
            page = AboutPage(self.page_container, page_id)

        else:
            page = MainPage(self.page_container, page_id)
            page.on("page/process", lambda text, page_id: self.process_text(text, page_id))
            page.on("page/create_cache", lambda page_id: self.create_cache(page_id))

        self.pages[page_id] = page
        return page

    def show_page(self, page_id):
        if page_id not in self.pages:
            raise ValueError(f"页面 ID '{page_id}' 未找到!")
        page = self.pages[page_id]

        for widget in self.page_container.winfo_children():
            widget.grid_forget()

        page.grid(row=0, column=0, sticky="nsew")

        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        return page

    def create_main(self, page_id):
        page = MainPage(self.page_container, page_id)
        page.on("page/process", lambda text, page_id: self.process_text(text, page_id))
        page.on("page/create_cache", lambda page_id: self.create_cache(page_id))

        return page

    def _update_tab_name(self, page_id, new_name):
        tab = self.tab_bar.get_tab_by_page_id(page_id)
        if tab:
            trimmed_name = new_name.strip()
            if len(trimmed_name) > 12:
                trimmed_name = trimmed_name[:12] + "..."
            tab.set_tab_name(trimmed_name if trimmed_name else f"Aba {page_id}")

    @show_loading_popup("正在登录，请稍候...", 50000)
    def _emit_login(self, input, page_id):
        self.emit("login", input, page_id)

    @after_decorator
    @close_loading_popup
    def handle_login_success(self, result):
        self.logged_in = True

        for pid in list(self.pages.keys()):
            if isinstance(self.pages[pid], LoginPage):
                self.pages[pid].destroy()
                del self.pages[pid]

                main_page = self.create_main(pid)
                self.pages[pid] = main_page
                main_page.grid(row=0, column=0, sticky="nsew")

        self.fetch_profile(result.get("page_id"))

    @show_loading_popup()
    def fetch_profile(self, page_id):
        self.emit("fetch_profile", page_id)

    @after_decorator
    def update_user_data(self, output):
        user_data = output['profile']
        self.label_id.config(text=f"ID: {user_data['id']}")
        self.label_role.config(text=f"Role: {user_data['role']}")
        self.label_email.config(text=f"User: {user_data['email']}")

    def logout(self):
        self.logged_in = False

        for pid in list(self.pages.keys()):
            if isinstance(self.pages[pid], MainPage):
                self.pages[pid].destroy()
                del self.pages[pid]

                login_page = LoginPage(self.page_container, pid)
                login_page.on("page/login", self._emit_login)
                self.pages[pid] = login_page
                login_page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.reset_footer()

    def reset_footer(self):
        self.label_id.config(text=f"ID: ")
        self.label_role.config(text=f"Role: ")
        self.label_email.config(text="User: ")

    @after_decorator
    @close_loading_popup
    def handle_error(self, error):
        messagebox.showerror("错误", error.get("error", "发生了一个未知的错误。"))

    @show_loading_popup()
    def process_text(self, text, page_id):
        self.emit("process", text, page_id)

    @after_decorator
    @close_loading_popup
    def handle_text_processed(self, result):
        page_id = result.get("page_id")
        processed_lines = result.get("results", [])
        page = self.pages.get(page_id)
        page.handle_text_processed(processed_lines)

    @show_loading_popup()
    def create_cache(self, page_id):
        file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel 文件", "*.xlsx *.xls")])
        if file_path:
            self.emit("create_cache", file_path, page_id)

    @after_decorator
    @close_loading_popup
    def handle_data_processed(self, result):
        processed_data = result.get("processed_data", [])

        with open("cache.json", "w", encoding="utf-8") as f:
            import json
            json.dump(processed_data, f, ensure_ascii=False, indent=4)