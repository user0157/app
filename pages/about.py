# 导入 tkinter 和 ttk 库，用于创建 GUI 界面
import tkinter as tk
from tkinter import ttk

# 导入自定义的 Page 类（假设它是应用程序页面的父类）
from pages.page import Page

# 导入 datetime 库，用于获取当前年份
import datetime

# 从配置文件导入应用程序名称、版本和作者信息
from config import APP_NAME, VERSION, AUTHOR

# 定义一个关于页面类 AboutPage，继承自 Page 类
class AboutPage(Page):
    # 创建页面的所有小部件
    def create_widgets(self):
        # 获取当前年份
        current_year = datetime.datetime.now().year
        
        # 定义关于页面要显示的文本内容，包含应用程序的名称、版本、作者和版权信息
        about_text = (
            f"程序名称: {APP_NAME}\n"  # 显示程序名称
            f"版本: {VERSION}\n"       # 显示程序版本
            f"作者: {AUTHOR}\n"        # 显示程序作者
            f"版权: © {current_year} {AUTHOR} 保留所有权利。\n"  # 显示版权信息，当前年份
            "感谢使用本程序！"  # 向用户表达感谢
        )

        # 创建一个标签控件（Label），显示关于页面的信息，设置文本居中显示
        self.label = ttk.Label(self, text=about_text, justify="center", anchor="center")

        # 使用 grid 布局管理器，设置标签的位置，并添加一些内边距
        self.label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # 配置 grid 布局，使该标签的行和列具有相同的权重，确保其在窗口大小调整时能够自适应
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
