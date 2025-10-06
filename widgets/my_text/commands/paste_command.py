# 导入 tkinter 模块，支持图形界面功能
import tkinter as tk
# 从当前包导入自定义的 Command 基类
from .command import Command

# 定义粘贴命令类，继承自 Command，符合命令模式
class PasteCommand(Command):
    # 执行粘贴操作的方法
    def execute(self):
        # 从剪贴板获取文本内容
        clipboard_text = self.widget.clipboard_get()

        if not clipboard_text:
            return  # 如果剪贴板为空，直接返回
        
        try:
            # 获取选中文本的起始索引
            start = self.widget.index(tk.SEL_FIRST)
            # 获取选中文本的结束索引
            end = self.widget.index(tk.SEL_LAST)
            
            # 使用 replace 方法覆盖选中文本为剪贴板内容
            self.widget.replace(start, end, clipboard_text)
        
        except tk.TclError:
            # 如果没有选中文本，selection_get 会抛出异常
            # 在光标位置插入剪贴板内容
            self.widget.insert(tk.INSERT, clipboard_text)
