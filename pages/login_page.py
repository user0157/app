# 导入 tkinter 和 ttk 库，用于创建 GUI 界面
import tkinter as tk
from tkinter import ttk, messagebox

# 导入 JSON 库，用于保存和加载凭据
import json

# 导入自定义的 Page 类（假设它是应用程序页面的父类）
from pages.page import Page

# 定义登录页面 LoginPage 类，继承自 Page 类
class LoginPage(Page):
    # 初始化方法，构造该页面，接收父窗口和页面ID
    def __init__(self, parent, page_id):
        super().__init__(parent, page_id)

    # 创建页面上的所有小部件
    def create_widgets(self):
        # 在创建小部件之前加载保存的凭据
        saved_credentials = self.load_saved_credentials()

        # 设置样式
        style = ttk.Style()
        # 配置一个样式 "Large.TEntry" 用于输入框，设置字体和内边距
        style.configure("Large.TEntry", padding=(5, 8, 5, 8), font=("微软雅黑", 14))

        # 初始化界面上的变量
        self.email_var = tk.StringVar()  # 用于绑定电子邮件输入框
        self.password_var = tk.StringVar()  # 用于绑定密码输入框
        self.show_password_var = tk.BooleanVar()  # 控制是否显示密码的复选框
        self.remember_me_var = tk.BooleanVar()  # 控制“记住用户名和密码”复选框

        # 配置页面的行和列，以适应窗口大小
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 创建背景框架
        self.bg_frame = tk.Frame(self, bg="#f2f2f2")
        self.bg_frame.grid(row=0, column=0, sticky="nsew")

        # 配置背景框架内部的行列配置
        self.bg_frame.grid_rowconfigure(0, weight=1)
        self.bg_frame.grid_columnconfigure(0, weight=1)

        # 创建中央对齐的容器，用于包含其他控件
        self.container = tk.Frame(self.bg_frame, bg="#ffffff", bd=2, relief="groove")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # 创建界面的小部件
        self._create_title()  # 创建标题
        self._create_email_input()  # 创建电子邮件输入框
        self._create_password_input()  # 创建密码输入框
        self._create_show_password_checkbox()  # 创建显示密码的复选框
        self._create_remember_me_checkbox()  # 创建记住密码的复选框
        self._create_login_button()  # 创建登录按钮

        # 聚焦到电子邮件输入框
        self.email_entry.focus()

        # 使用保存的凭据填充输入框（如果有的话）
        self.fill_credentials(saved_credentials)

    # 创建标题标签
    def _create_title(self):
        title = tk.Label(self.container, text="用户登录", font=("微软雅黑", 18, "bold"), bg="#ffffff")
        title.grid(row=0, column=0, pady=(20, 10), padx=20)

    # 创建电子邮件输入框及其标签
    def _create_email_input(self):
        label = tk.Label(self.container, text="电子邮件:", font=("微软雅黑", 10), bg="#ffffff")
        label.grid(row=1, column=0, sticky="w", padx=20, pady=(5, 0))

        self.email_entry = ttk.Entry(self.container, textvariable=self.email_var, width=35, style="Large.TEntry")
        self.email_entry.grid(row=2, column=0, padx=20, pady=(0, 10))

    # 创建密码输入框及其标签
    def _create_password_input(self):
        label = tk.Label(self.container, text="密码:", font=("微软雅黑", 10), bg="#ffffff")
        label.grid(row=3, column=0, sticky="w", padx=20, pady=(5, 0))

        self.password_entry = ttk.Entry(self.container, textvariable=self.password_var, show="*", width=35, style="Large.TEntry")
        self.password_entry.grid(row=4, column=0, padx=20, pady=(0, 10))
        # 按回车键执行登录操作
        self.password_entry.bind("<Return>", lambda event: self.login())

    # 创建显示密码的复选框
    def _create_show_password_checkbox(self):
        checkbox = tk.Checkbutton(
            self.container,
            text="显示密码",  # 显示密码复选框
            font=("微软雅黑", 9),
            variable=self.show_password_var,
            bg="#ffffff",
            command=self._toggle_password_visibility  # 切换密码显示与否
        )
        checkbox.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 10))

    # 创建记住用户名和密码的复选框
    def _create_remember_me_checkbox(self):
        checkbox = tk.Checkbutton(
            self.container,
            text="记住用户名和密码",  # 记住凭据复选框
            font=("微软雅黑", 9),
            variable=self.remember_me_var,
            bg="#ffffff"
        )
        checkbox.grid(row=6, column=0, sticky="w", padx=20, pady=(0, 10))

    # 创建登录按钮
    def _create_login_button(self):
        button = ttk.Button(self.container, text="登录", command=self.login)
        button.grid(row=7, column=0, pady=(0, 20), padx=20)

    # 切换密码输入框的显示/隐藏
    def _toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")  # 显示密码
        else:
            self.password_entry.config(show="*")  # 隐藏密码

    # 执行登录操作
    def login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        # 输入验证：检查电子邮件和密码是否为空
        if not email or not password:
            messagebox.showwarning("警告", "请输入电子邮件和密码。")
            return

        # 如果选中“记住”选项，保存凭据
        if self.remember_me_var.get():
            self.save_credentials(email, password)
        else:
            self.clear_saved_credentials()

        # 发送登录请求
        input_data = {"email": email, "password": password}
        self.emit("page/login", input_data, self.page_id)

    # 将凭据保存到 JSON 文件中
    def save_credentials(self, email, password):
        data = {
            "email": email,
            "password": password,
            "remember_me": self.remember_me_var.get()
        }
        with open("credentials.json", "w") as f:
            json.dump(data, f)

    # 从 JSON 文件中加载保存的凭据
    def load_saved_credentials(self):
        try:
            with open("credentials.json", "r") as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None  # 没有保存的凭据或读取 JSON 文件时出错

    # 使用保存的凭据填充输入框
    def fill_credentials(self, data):
        if data:
            self.email_var.set(data.get("email", ""))
            self.password_var.set(data.get("password", ""))
            self.remember_me_var.set(data.get("remember_me", False))

    # 清除保存的凭据
    def clear_saved_credentials(self):
        try:
            with open("credentials.json", "w") as f:
                json.dump({}, f)  # 清空 JSON 文件内容
        except FileNotFoundError:
            pass
