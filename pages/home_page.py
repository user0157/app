# 导入 tkinter 和 ttk 库，用于创建 GUI 界面
import tkinter as tk
from tkinter import ttk, messagebox

# 导入自定义的 Page 类（假设它是应用程序页面的父类）
from pages.page import Page

# 定义一个首页 HomePage 类，继承自 Page 类
class HomePage(Page):
    # 初始化方法，构造该页面，接收主窗口（master）和页面ID（page_id）
    def __init__(self, master=None, page_id=None):
        # 调用父类 Page 的初始化方法，初始化父类的一些属性
        super().__init__(master, page_id)
        # 使用 grid 布局管理器，并让该页面适应父级窗口的大小
        self.grid(sticky="nsew")
        # 创建页面上的所有小部件
        self.create_widgets()

    # 创建页面上的所有小部件
    def create_widgets(self):
        # 创建一个容器 Frame，用来包含页面上的所有控件
        container = ttk.Frame(self)
        # 使用 grid 布局管理器，将容器放在窗口的 0 行 0 列，并设置内边距
        container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # 创建一个样式对象，定义控件的外观
        style = ttk.Style()
        # 配置标签的字体样式：使用 Microsoft YaHei 字体，字号 16，加粗
        style.configure("Custom.TLabel", font=("Microsoft YaHei", 16, "bold"))
        # 配置按钮的字体样式：使用 Microsoft YaHei 字体，字号 12
        style.configure("Custom.TButton", font=("Microsoft YaHei", 12))

        # 创建一个标签控件，显示 "开始" 文字
        self.label = ttk.Label(container, text="开始", style="Custom.TLabel")
        # 使用 grid 布局将标签放置在 0 行 0 列，设置上下间距（pady=(0, 20)）
        self.label.grid(row=0, column=0, pady=(0, 20))

        # 定义一个页面按钮的列表，每个元组包含按钮文本和对应的页面类型
        page_buttons = [
            ("打开匹配价格界面", "process"),  # 打开匹配价格页面
            ("库存管理界面", "inventory"),    # 打开库存管理页面
            ("关于", "about")                 # 打开关于页面
        ]

        # 遍历页面按钮列表，动态创建按钮并放置在页面上
        for idx, (button_text, page_type) in enumerate(page_buttons):
            # 创建按钮，绑定 `open_page` 方法，并传入按钮的页面类型
            button = ttk.Button(container, text=button_text, command=lambda type=page_type: self.open_page(type), style="Custom.TButton")
            # 使用 grid 布局将按钮放置在不同的行，设置上下间距（pady=10），并使按钮在水平方向上填充整个宽度（sticky="ew"）
            button.grid(row=idx + 1, column=0, pady=10, sticky="ew")

        # 配置容器的列宽，以确保按钮能够横向填充整个容器
        container.columnconfigure(0, weight=1)
        # 配置页面的列宽，以确保容器能够自适应父窗口大小
        self.columnconfigure(0, weight=1)

    # 打开指定类型的页面方法
    def open_page(self, type):
        # 通过 `emit` 方法通知父类或事件处理系统，触发页面切换
        self.emit("open_page", type)
