# 导入 tkinter 和 ttk 库，用于创建 GUI 框架和样式控件
import tkinter as tk
from tkinter import ttk

# 导入事件管理类，用于事件的注册、触发和监听
from event_emitter import EventEmitter

# =========================
# 页面类：作为所有页面的基类
# =========================
class Page(ttk.Frame, EventEmitter):
    def __init__(self, parent, page_id):
        # 初始化 ttk.Frame（GUI 组件）
        ttk.Frame.__init__(self, parent)
        
        # 初始化 EventEmitter（事件发射器，用于事件通信）
        EventEmitter.__init__(self)

        # 页面唯一标识符
        self.page_id = page_id

        # 设置页面的行列权重，确保自适应窗口大小
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 创建控件（由子类实现）
        self._create_widgets()

        # 绑定事件（由子类实现）
        self._bind_events()

    # 占位方法：由子类实现界面元素的创建逻辑
    def create_widgets(self):
        pass

    # 占位方法：由子类实现事件绑定逻辑（比如按钮点击、键盘事件等）
    def bind_events(self):
        pass

    # 占位方法：由子类实现页面内容的更新逻辑（可能用于刷新显示等）
    def update(self):
        pass

    # 私有方法：调用子类实现的 create_widgets
    def _create_widgets(self):
        self.create_widgets()

    # 私有方法：绑定默认和自定义事件
    def _bind_events(self):
        # 监听名为 "processed" 的事件，事件触发后调用 _update 方法
        self.on("processed", self._update)

        # 调用子类自定义的事件绑定方法
        self.bind_events()

    # 私有方法：被 "processed" 事件触发后执行，用于更新页面
    def _update(self, result):
        # 调用子类的 update 方法，传入结果参数
        self.update(result)
