# 导入 tkinter 模块以支持 GUI 功能
import tkinter as tk

# 从当前包导入自定义的 Command 基类
from .command import Command

# 剪切命令类，继承自 Command，遵循命令模式
class CutCommand(Command):
    # 执行剪切操作
    def execute(self):
        try:
            # 获取当前选中的文本
            selected_text = self.widget.selection_get()
            
            # 清空剪贴板内容
            self.widget.clipboard_clear()
            
            # 将选中的文本复制到剪贴板
            self.widget.clipboard_append(selected_text)
            
            # 从文本组件中删除选中的文本，实现剪切效果
            self.widget.delete("sel.first", "sel.last")
        
        # 如果没有选中的文本或其他错误，捕获并忽略异常
        except tk.TclError:
            pass
