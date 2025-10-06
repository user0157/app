import re
from .quadruple_click import QuadrupleClickText
from .replace import TextWithReplace

class MyText(QuadrupleClickText, TextWithReplace):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.config(wrap="word", font=("Microsoft YaHei", 14), undo=True)
        
        self.context_menu.add_command(label="标记数量", command=self.wrap_selected_quantity)
        self.context_menu.add_command(label="标记价格", command=self.wrap_selected_price)

    def is_valid_number(self, text):
        return re.fullmatch(r"\d+(?:[.,]\d+)?", text) is not None

    def wrap_selected_quantity(self):
        try:
            selected_text = self.get("sel.first", "sel.last").replace(" ", "")
            if self.is_valid_number(selected_text):
                new_text = f"[quantity:{selected_text}]"
                self.delete("sel.first", "sel.last")
                self.insert("insert", new_text)
            else:
                print("请选择一个有效的数字（可以包含小数点、逗号或空格）。")
        except Exception as e:
            print(f"未选择任何文本或发生错误: {e}")

    def wrap_selected_price(self):
        try:
            selected_text = self.get("sel.first", "sel.last").replace(" ", "")
            if self.is_valid_number(selected_text):
                new_text = f"[price:{selected_text}]"
                self.delete("sel.first", "sel.last")
                self.insert("insert", new_text)
            else:
                print("请选择一个有效的数字（可以包含小数点、逗号或空格）。")
        except Exception as e:
            print(f"未选择任何文本或发生错误: {e}")

