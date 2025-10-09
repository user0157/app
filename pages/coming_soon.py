# 导入 tkinter 和 ttk 库，用于创建 GUI 界面
import tkinter as tk
from tkinter import ttk

# 导入自定义的 Page 类（假设它是应用程序页面的父类）
from pages.page import Page

# 定义一个 ComingSoon 页面类，继承自 Page 类
class ComingSoon(Page):
    # 初始化方法，构造该页面，接收父窗口和页面ID
    def __init__(self, parent, page_id):
        # 调用父类 Page 的初始化方法，初始化父类的一些属性
        super().__init__(parent, page_id)
        
    # 创建页面上的所有小部件
    def create_widgets(self):
        # 创建一个标签控件（Label），用于显示 "此功能尚未实现" 的消息
        # 设置字体为 Arial，字号 20，字体加粗
        self.message_label = ttk.Label(self, text="此功能尚未实现", font=("Arial", 20, "bold"))
        
        # 使用 grid 布局管理器，设置标签的位置，并添加一些内边距
        self.message_label.grid(row=0, column=0, padx=10, pady=10)
