import tkinter as tk
from .base_text import BaseText

class TextWithHighlight(BaseText):
    """
    支持词语高亮的文本框组件：
    - 自动高亮选中文本或光标下的完整词语的所有匹配项
    - 使用边界检测，避免光标在标点后高亮错误词语
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # 配置高亮和自定义选中样式
        self.tag_configure("highlight", background='lightgreen', foreground="black")
        self.tag_configure("custom_sel", background='lightblue', foreground="black")

        # 绑定事件，当光标移动或选中变化时触发高亮逻辑
        self.bind("<KeyRelease>", self.on_cursor_or_selection_change)
        self.bind("<ButtonRelease>", self.on_cursor_or_selection_change)
        self.bind("<<Selection>>", self.on_cursor_or_selection_change)
        self.bind("<Motion>", self.on_cursor_or_selection_change)

    def on_cursor_or_selection_change(self, event=None):
        self.highlight_selection_or_word()
        
    def get_current_word(self):
        """
        检测光标所在位置的当前单词，支持光标在单词前、中、后的位置
        避免跨行检测单词
        返回 (单词起始索引, 单词结束索引, 单词字符串)
        如果未找到单词，则返回 (None, None, "")
        """
        try:
            cursor_index = self.index("insert")
            cursor_line = int(cursor_index.split('.')[0])  # 记录光标当前行号
            
            candidates = [
                cursor_index,
                self.index(f"{cursor_index} -1c"),
                self.index(f"{cursor_index} +1c"),
            ]
            
            for idx in candidates:
                line = int(idx.split('.')[0])
                # 只处理同一行的索引，避免检测到下一行单词
                if line != cursor_line:
                    continue
                
                try:
                    word_start = self.index(f"{idx} wordstart")
                    word_end = self.index(f"{idx} wordend")
                    word = self.get(word_start, word_end)
                    if word.strip() and any(c.isalnum() or '\u4e00' <= c <= '\u9fff' for c in word):
                        return word_start, word_end, word
                except tk.TclError:
                    continue
        except tk.TclError:
            pass
        
        return None, None, ""

    def highlight_selection_or_word(self):
        """
        高亮当前选中词或光标下完整词语的所有匹配项
        - 避免光标在标点或空格后错误高亮前面单词
        """
        self.tag_remove("highlight", "1.0", tk.END)
        self.tag_remove("custom_sel", "1.0", tk.END)

        try:
            self.selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            sel_start = self.index(tk.SEL_FIRST)
            sel_end = self.index(tk.SEL_LAST)
        except tk.TclError:
            self.selected_text = ""
            sel_start = sel_end = None

        if self.selected_text.strip():
            self.tag_add("custom_sel", sel_start, sel_end)
            word = self.selected_text.strip()
        else:
            word_start, word_end, word = self.get_current_word()
            if not word:
                return

        if not word.strip():
            return

        cursor_index = self.index(tk.INSERT)  # 获取当前光标位置
        start = "1.0"
        word_len = len(word)

        while True:
            pos = self.search(word, start, stopindex=tk.END, nocase=True)
            if not pos:
                break

            # 检查前后字符是否为词语边界
            before = self.get(f"{pos} -1c", pos)
            after = self.get(f"{pos} +{word_len}c", f"{pos} +{word_len + 1}c")

            def is_boundary(c):
                return not (c.isalnum() or '\u4e00' <= c <= '\u9fff')

            if (is_boundary(before) or before == "") and (is_boundary(after) or after == ""):
                end = f"{pos}+{word_len}c"

                # 避免重复高亮当前选中区域
                if sel_start and sel_end:
                    if self.compare(pos, ">=", sel_start) and self.compare(pos, "<", sel_end):
                        start = end
                        continue

                self.tag_add("highlight", pos, end)

            start = f"{pos}+1c"
