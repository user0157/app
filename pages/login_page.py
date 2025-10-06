import tkinter as tk
from tkinter import ttk, messagebox
import json
from pages.page import Page

class LoginPage(Page):
    def __init__(self, parent, page_id):
        super().__init__(parent, page_id)

    def create_widgets(self):
        # 在创建小部件之前加载保存的凭据
        saved_credentials = self.load_saved_credentials()

        # 设置样式
        style = ttk.Style()
        style.configure("Large.TEntry", padding=(5, 8, 5, 8), font=("微软雅黑", 14))

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar()
        self.remember_me_var = tk.BooleanVar()  # "记住用户名和密码" 选项

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bg_frame = tk.Frame(self, bg="#f2f2f2")
        self.bg_frame.grid(row=0, column=0, sticky="nsew")

        self.bg_frame.grid_rowconfigure(0, weight=1)
        self.bg_frame.grid_columnconfigure(0, weight=1)

        # 中央对齐的容器
        self.container = tk.Frame(self.bg_frame, bg="#ffffff", bd=2, relief="groove")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # 创建界面的小部件
        self._create_title()
        self._create_email_input()
        self._create_password_input()
        self._create_show_password_checkbox()
        self._create_remember_me_checkbox()  # 添加“记住”的选项
        self._create_login_button()

        self.email_entry.focus()  # 聚焦到电子邮件输入框

        # 使用保存的凭据填充输入框（如果有的话）
        self.fill_credentials(saved_credentials)

    def _create_title(self):
        # 设置标题
        title = tk.Label(self.container, text="用户登录", font=("微软雅黑", 18, "bold"), bg="#ffffff")  # Título traduzido
        title.grid(row=0, column=0, pady=(20, 10), padx=20)

    def _create_email_input(self):
        # 设置电子邮件输入框标签
        label = tk.Label(self.container, text="电子邮件:", font=("微软雅黑", 10), bg="#ffffff")  # Rótulo do email traduzido
        label.grid(row=1, column=0, sticky="w", padx=20, pady=(5, 0))

        # 电子邮件输入框
        self.email_entry = ttk.Entry(self.container, textvariable=self.email_var, width=35, style="Large.TEntry")
        self.email_entry.grid(row=2, column=0, padx=20, pady=(0, 10))

    def _create_password_input(self):
        # 设置密码输入框标签
        label = tk.Label(self.container, text="密码:", font=("微软雅黑", 10), bg="#ffffff")  # Rótulo da senha traduzido
        label.grid(row=3, column=0, sticky="w", padx=20, pady=(5, 0))

        # 密码输入框
        self.password_entry = ttk.Entry(self.container, textvariable=self.password_var, show="*", width=35, style="Large.TEntry")
        self.password_entry.grid(row=4, column=0, padx=20, pady=(0, 10))
        self.password_entry.bind("<Return>", lambda event: self.login())  # 按回车键登录

    def _create_show_password_checkbox(self):
        # 创建显示密码的复选框
        checkbox = tk.Checkbutton(
            self.container,
            text="显示密码",  # Mostrar Senha traduzido
            font=("微软雅黑", 9),
            variable=self.show_password_var,
            bg="#ffffff",
            command=self._toggle_password_visibility
        )
        checkbox.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 10))

    def _create_remember_me_checkbox(self):
        # 创建“记住用户名和密码”的复选框
        checkbox = tk.Checkbutton(
            self.container,
            text="记住用户名和密码",  # Lembrar usuário e senha traduzido
            font=("微软雅黑", 9),
            variable=self.remember_me_var,
            bg="#ffffff"
        )
        checkbox.grid(row=6, column=0, sticky="w", padx=20, pady=(0, 10))

    def _create_login_button(self):
        # 创建登录按钮
        button = ttk.Button(self.container, text="登录", command=self.login)  # Login traduzido
        button.grid(row=7, column=0, pady=(0, 20), padx=20)

    def _toggle_password_visibility(self):
        # 切换密码的显示/隐藏
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        # 基本的输入验证
        if not email or not password:
            messagebox.showwarning("警告", "请输入电子邮件和密码。")  # Mensagem de alerta traduzida
            return

        # 如果选中“记住”选项，保存凭据
        if self.remember_me_var.get():
            self.save_credentials(email, password)
        else:
            self.clear_saved_credentials()

        # 发送登录数据
        input_data = {"email": email, "password": password}
        self.emit("page/login", input_data, self.page_id)

    def save_credentials(self, email, password):
        # 将凭据和“记住”选项保存到JSON文件中
        data = {
            "email": email,
            "password": password,
            "remember_me": self.remember_me_var.get()
        }
        with open("credentials.json", "w") as f:
            json.dump(data, f)

    def load_saved_credentials(self):
        # 从JSON文件加载保存的凭据和“记住”选项
        try:
            with open("credentials.json", "r") as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None  # 没有保存的凭据或读取JSON文件时出错

    def fill_credentials(self, data):
        # 使用保存的凭据填充输入框
        if data:
            self.email_var.set(data.get("email", ""))
            self.password_var.set(data.get("password", ""))
            self.remember_me_var.set(data.get("remember_me", False))  # 如果保存了“记住”选项，则选中它

    def clear_saved_credentials(self):
        # 清除保存的凭据（如果用户取消了“记住”选项）
        try:
            with open("credentials.json", "w") as f:
                json.dump({}, f)  # 清空JSON文件的内容
        except FileNotFoundError:
            pass
