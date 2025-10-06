import tkinter as tk
from .commands import CutCommand, CopyCommand, PasteCommand

class BaseText(tk.Text):
    """
    自定义文本框类，添加了右键菜单功能
    继承自 tk.Text，提供剪切、复制、粘贴等基本编辑功能
    """
    def __init__(self, master, **kwargs):
        """
        初始化文本框，配置样式，并创建右键菜单
        :param master: 父容器
        :param kwargs: Text 组件的其他配置参数
        """
        super().__init__(master, **kwargs)

        # 创建右键菜单
        self.context_menu = self.create_context_menu()

        # 将鼠标右键（Button-3）事件绑定到菜单显示函数
        self.bind("<Button-3>", self.show_context_menu)

    def overwrite(self, new_text: str):
        self.replace("1.0", "end", new_text)

    def create_context_menu(self):
        """
        创建并返回右键菜单（剪切、复制、粘贴）
        :return: tk.Menu 对象
        """
        self.context_menu = tk.Menu(self, tearoff=0, font=("Microsoft YaHei", 12))

        commands = {
            "剪切": CutCommand(self),
            "复制": CopyCommand(self),
            "粘贴": PasteCommand(self)
        }

        for label, command in commands.items():
            self.context_menu.add_command(label=label, command=command.execute)

        return self.context_menu

    def show_context_menu(self, event):
        try:
            selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected_text = None

        if not selected_text:
            # 获取点击位置对应的索引（字符左边界）
            index = self.index(f"@{event.x},{event.y}")

            # 获取该字符的边界框（返回：x, y, width, height）
            bbox = self.bbox(index)

            if bbox:
                x_char, y_char, width_char, height_char = bbox
                # 计算点击点在字符内的偏移
                offset_x = event.x - x_char

                # 如果点击位置偏右，光标右移一格
                if offset_x > width_char / 2:
                    # 获取下一个字符索引
                    next_index = self.index(f"{index} +1c")
                    self.mark_set(tk.INSERT, next_index)
                else:
                    self.mark_set(tk.INSERT, index)
            else:
                # 如果无法获取字符边界，退回默认行为
                self.mark_set(tk.INSERT, index)

        self.focus_set()
        self.context_menu.tk_popup(event.x_root, event.y_root)

