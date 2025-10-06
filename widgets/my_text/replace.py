import tkinter as tk
from .highlight import TextWithHighlight

class TextWithReplace(TextWithHighlight):
    """
    在高亮基础上添加：
    - 右键菜单选项：
        - 替换所有匹配项（包含部分词）
        - 重命名符号（仅完整词）
    - 内联输入框进行替换
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # 添加右键菜单项（中文）
        self.context_menu.add_command(label="替换所有匹配项", command=self.replace_all_partial)
        self.context_menu.add_command(label="重命名符号", command=self.replace_all_exact)

    def replace_all_partial(self):
        self.replacement_mode = "partial"
        self.open_inline_entry()

    def replace_all_exact(self):
        self.replacement_mode = "exact"
        self.open_inline_entry()

    def open_inline_entry(self):
        try:
            if self.tag_ranges(tk.SEL):
                self.selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
                start_index = self.index(tk.SEL_FIRST)
            else:
                word_start, _, word = self.get_current_word()
                if not word:
                    return
                self.selected_text = word
                start_index = word_start
        except tk.TclError:
            return

        bbox = self.bbox(start_index)
        if not bbox:
            return

        x, y, width, height = bbox
        relative_x = self.winfo_rootx() - self.master.winfo_rootx() + x
        relative_y = self.winfo_rooty() - self.master.winfo_rooty() + y + height + 3

        self.inline_entry = tk.Entry(self.master, font=("Microsoft YaHei", 14))
        self.inline_entry.place(x=relative_x, y=relative_y,
                                width=max(150, width * 1.3), height=height + 4)
        self.inline_entry.insert(0, self.selected_text)
        self.inline_entry.select_range(0, tk.END)
        self.inline_entry.focus_set()

        self.inline_entry.bind("<Return>", self.on_inline_entry_confirm)
        self.inline_entry.bind("<Escape>", self.on_inline_entry_cancel)
        self.inline_entry.bind("<FocusOut>", self.on_inline_entry_cancel)

    def on_inline_entry_confirm(self, event=None):
        if self.inline_entry:
            new_value = self.inline_entry.get()
            old_value = getattr(self, "selected_text", None)
            mode = getattr(self, "replacement_mode", "exact")

            if old_value:
                if mode == "exact":
                    self.replace_terms_exact(old_value, new_value)
                else:
                    self.replace_terms_partial(old_value, new_value)

            self.inline_entry.destroy()
            self.inline_entry = None

        self.focus_set()

    def on_inline_entry_cancel(self, event=None):
        if self.inline_entry:
            self.inline_entry.destroy()
            self.inline_entry = None

    def replace_terms_exact(self, old_value, new_value):
        """
        仅替换完整词语（符号），忽略部分匹配
        """
        if not old_value:
            return

        self.edit_separator()
        self.configure(autoseparators=False)

        start = "1.0"
        word_len = len(old_value)

        while True:
            pos = self.search(old_value, start, stopindex=tk.END, nocase=False)
            if not pos:
                break

            before = self.get(f"{pos} -1c", pos)
            after = self.get(f"{pos} +{word_len}c", f"{pos} +{word_len + 1}c")

            def is_boundary(c):
                return not (c.isalnum() or '\u4e00' <= c <= '\u9fff')

            if (is_boundary(before) or before == "") and (is_boundary(after) or after == ""):
                end_pos = f"{pos}+{word_len}c"
                self.delete(pos, end_pos)
                self.insert(pos, new_value)
                start = f"{pos}+{len(new_value)}c"
            else:
                start = f"{pos}+1c"

        self.configure(autoseparators=True)
        self.edit_separator()

    def replace_terms_partial(self, old_value, new_value):
        """
        替换所有匹配项（包括词语内部）
        """
        if not old_value:
            return

        self.edit_separator()
        self.configure(autoseparators=False)

        start = "1.0"
        while True:
            pos = self.search(old_value, start, stopindex=tk.END, nocase=False)
            if not pos:
                break

            end_pos = f"{pos}+{len(old_value)}c"
            self.delete(pos, end_pos)
            self.insert(pos, new_value)
            start = f"{pos}+{len(new_value)}c"

        self.configure(autoseparators=True)
        self.edit_separator()
