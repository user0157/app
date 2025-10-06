# 导入 tkinter 模块，并导入 Command 基类
import tkinter as tk
from .command import Command

# 复制命令类，继承自 Command 基类
class CopyCommand(Command):
    # 执行复制操作
    def execute(self):
        try:
            # 获取当前选中的文本
            selected_text = self.widget.selection_get()
            # 清空剪贴板内容
            self.widget.clipboard_clear()
            # 将选中的文本追加到剪贴板中
            self.widget.clipboard_append(selected_text)
        # 如果没有选中的文本，会抛出 TclError，此时忽略错误
        except tk.TclError:
            pass
