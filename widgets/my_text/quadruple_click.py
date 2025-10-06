import tkinter as tk

class QuadrupleClickText(tk.Text):
    """
    支持四击全选的自定义文本框
    继承自tk.Text，添加了四击全选功能
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # 初始化点击计数器，记录连续点击次数
        self.click_count = 0
        # 记录上一次点击的时间，用于判断连续点击间隔
        self.last_click_time = 0
        
        # 绑定鼠标左键点击事件
        # add=True 确保不会覆盖已有绑定事件
        self.bind('<Button-1>', self.on_click, add=True)
    
    def on_click(self, event):
        """处理鼠标左键点击事件"""
        # 获取当前点击事件的时间戳（毫秒）
        current_time = event.time
        
        # 如果距离上次点击超过500毫秒，重置点击计数
        if self.last_click_time and (current_time - self.last_click_time > 500):
            self.click_count = 0
        
        # 增加点击计数
        self.click_count += 1
        # 更新时间戳为当前点击时间
        self.last_click_time = current_time
        
        # 当检测到连续四次点击时，执行全选操作
        if self.click_count == 4:
            self.select_all()
            # 重置点击计数，防止重复触发
            self.click_count = 0
            # 返回 "break" 阻止事件继续传播，避免默认行为干扰
            return "break"
    
    def select_all(self):
        """全选文本框中的所有内容"""
        # 先移除之前的选择区域
        self.tag_remove(tk.SEL, "1.0", tk.END)
        # 添加新的选择区域，从文本开始到末尾
        self.tag_add(tk.SEL, "1.0", tk.END)
        # 将插入点移动到文本末尾
        self.mark_set(tk.INSERT, tk.END)
        # 确保插入点可见
        self.see(tk.INSERT)
        # 将焦点设置到文本框
        self.focus_set()