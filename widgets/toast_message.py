import tkinter as tk

class ToastMessage(tk.Toplevel):
    """
    Toast消息提示窗口类
    继承自tkinter.Toplevel,用于显示临时弹出的提示信息
    """
    def __init__(self, master, msg, duration=500, fade_steps=10, **kwargs):
        """
        初始化Toast消息窗口
        
        参数:
            master: 父窗口
            msg: 要显示的消息文本
            duration: 消息显示持续时间(毫秒)
            fade_steps: 淡入淡出的步数
            bg: 背景色
            fg: 文字颜色
            font: 字体设置
        """
        super().__init__(master)
        self.overrideredirect(True)  # 去除窗口边框
        self.attributes("-topmost", True)  # 设置窗口置顶
        self.attributes("-alpha", 0.0)  # 初始化时完全透明

        if 'font' not in kwargs:
            kwargs['font'] = ('Microsoft YaHei', 14)

        # 创建标签显示消息
        self.label = tk.Label(self, text=msg, padx=10, pady=5, **kwargs)
        self.label.pack()

        self.update_idletasks()

        # 计算Toast窗口位置,使其在主窗口底部居中显示
        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_w = master.winfo_width()
        master_h = master.winfo_height()
        toast_w = self.winfo_width()
        toast_h = self.winfo_height()

        x = master_x + (master_w - toast_w) // 2
        y = master_y + master_h - toast_h - 30
        self.geometry(f"+{x}+{y}")

        # 设置动画参数
        self.fade_in_step = 1 / fade_steps  # 淡入步长
        self.fade_out_step = 1 / fade_steps  # 淡出步长
        self.duration = duration  # 显示持续时间
        self.fade_in()  # 开始淡入动画
        master.focus_force()  # 强制获取焦点

    def fade_in(self, alpha=0.0):
        """
        淡入动画效果
        通过逐步增加窗口透明度实现
        
        参数:
            alpha: 当前透明度值
        """
        alpha = round(alpha + self.fade_in_step, 2)
        if alpha >= 1.0:
            self.attributes("-alpha", 1.0)
            self.after(self.duration, self.fade_out)  # 完全显示后等待指定时间开始淡出
        else:
            self.attributes("-alpha", alpha)
            self.after(30, lambda: self.fade_in(alpha))

    def fade_out(self, alpha=1.0):
        """
        淡出动画效果
        通过逐步减少窗口透明度实现
        
        参数:
            alpha: 当前透明度值
        """
        alpha = round(alpha - self.fade_out_step, 2)
        if alpha <= 0.0:
            self.destroy()  # 完全透明后销毁窗口
        else:
            self.attributes("-alpha", alpha)
            self.after(30, lambda: self.fade_out(alpha))
