from .base_plugin import BasePlugin
import tkinter as tk

class CellPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

    def run(self):
        self.tree.bind("<Button-3>", self.open_menu, add=True)

    def open_menu(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)

            if not item or not column:
                return
            
            self.tree.selection_set(item)

            popup_menu = tk.Menu(self.table, tearoff=0)
            popup_menu.add_command(label="添加上方行", command=lambda: self.add_row_above(item))
            popup_menu.add_command(label="添加下方行", command=lambda: self.add_row_below(item))
            popup_menu.add_command(label="删除行", command=lambda: self.remove_row(item))

            popup_menu.post(event.x_root, event.y_root)

    def get_row_index(self, row_id):
        return next((i for i, d in enumerate(self.data) if d.get('row_id') == row_id), None)

    def add_row_above(self, row_id):
        if row_id:
            index = self.get_row_index(row_id)
            self.table.add_row(index=index)

    def add_row_below(self, row_id):
        if row_id:
            index = self.get_row_index(row_id) + 1
            self.table.add_row(index=index)

    def remove_row(self, row_id):
        if row_id:
            index = self.get_row_index(row_id)
            self.table.remove_row(index=index)
